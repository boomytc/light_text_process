const boot = window.__LIGHT_TEXT_PROCESSING_BOOT__ || {};
let capabilities = boot.capabilities || { operations: {} };

const state = {
  operation: "tn",
  currentView: "process",
  examples: [],
  exampleFilter: "all",
  batchRows: [],
  toastTimer: null,
};

const endpointMap = {
  tn: { method: "POST", url: "/api/v1/tn" },
  itn: { method: "POST", url: "/api/v1/itn" },
  num2words: { method: "POST", url: "/api/v1/num2words" },
  batch: { method: "POST", url: "/api/v1/batch" },
  capabilities: { method: "GET", url: "/api/v1/capabilities" },
};

const defaults = {
  tn: { language: "zh", input: "今天是 2026 年 6 月 15 日。\n我有 123 元。" },
  itn: { language: "zh", input: "二零二六年六月十五日\n我有一百二十三元" },
  num2words: { language: "en", input: "12345\n2026" },
};

const $ = (id) => document.getElementById(id);
const entries = (value) => Object.entries(value || {});

function setStatus(text, isError = false) {
  const chip = $("status-chip");
  chip.textContent = text;
  chip.classList.toggle("is-error", isError);
}

function toast(message, isError = false) {
  const node = $("toast");
  window.clearTimeout(state.toastTimer);
  node.textContent = message;
  node.classList.toggle("error", isError);
  node.classList.remove("hidden");
  state.toastTimer = window.setTimeout(() => node.classList.add("hidden"), 2600);
}

function operationConfig(operation = state.operation) {
  return capabilities.operations?.[operation] || {};
}

function operationLabel(operation = state.operation) {
  const config = operationConfig(operation);
  return config.display_label || config.label || operation;
}

function languageLabel(language, operation = state.operation) {
  const label = operationConfig(operation).languages?.[language];
  if (!label || label === language) return language;
  return `${language} - ${label}`;
}

function fillSelect(select, values, selected) {
  select.innerHTML = "";
  for (const [value, label] of entries(values)) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label === value ? value : `${value} - ${label}`;
    if (value === selected) option.selected = true;
    select.appendChild(option);
  }
}

function selectedLanguage() {
  return $("language-select").value;
}

function setOperation(operation, preserveInput = false) {
  state.operation = operation;
  $("operation-select").value = operation;

  $("tn-options").classList.toggle("hidden", operation !== "tn");
  $("itn-options").classList.toggle("hidden", operation !== "itn");
  $("num2words-options").classList.toggle("hidden", operation !== "num2words");
  $("advanced-options").classList.toggle("hidden", false);

  const languages = operationConfig(operation).languages || {};
  const defaultLanguage = defaults[operation]?.language || Object.keys(languages)[0] || "zh";
  const currentLanguage = selectedLanguage();
  const selected = Object.hasOwn(languages, currentLanguage) ? currentLanguage : defaultLanguage;
  fillSelect($("language-select"), languages, selected);

  $("operation-help").textContent = operationConfig(operation).help_text || operationConfig(operation).description || "";
  $("process-tool-title").textContent = operation === "num2words" ? "数字转外语词" : operationLabel(operation);
  $("input-label").textContent = operation === "num2words" ? "数字" : "输入";
  $("input-hint").textContent = operation === "num2words" ? "每行一个数字；单条直接输入一行。" : "每行一条；单条直接输入一行。";

  if (!preserveInput) {
    $("process-input").value = defaults[operation]?.input || "";
  }
  syncLanguageScopedControls();
  clearResults();
  updateApiPreview();
}

function setView(view) {
  state.currentView = view;
  document.querySelectorAll("[data-view]").forEach((button) => {
    const active = button.dataset.view === view;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
  });
  $("process-view").classList.toggle("hidden", view !== "process");
  $("examples-view").classList.toggle("hidden", view !== "examples");
  $("api-view").classList.toggle("hidden", view !== "api");
  if (view === "api") updateApiPreview();
}

function intValue(id, fallback) {
  const value = Number.parseInt($(id).value, 10);
  return Number.isFinite(value) ? value : fallback;
}

function tnOptions() {
  return {
    input_case: $("input-case-select").value,
    deterministic: $("tn-deterministic").checked,
    whitelist_path: $("tn-whitelist").value.trim() || null,
    post_process: $("tn-post-process").checked,
    punct_pre_process: $("tn-punct-pre").checked,
    punct_post_process: $("tn-punct-post").checked,
    batch_size: intValue("tn-batch-size", 1),
    n_jobs: intValue("tn-n-jobs", 1),
  };
}

function itnOptions() {
  return {
    enable_standalone_number: $("itn-standalone-number").checked,
    enable_0_to_9: $("itn-zero-to-nine").checked,
  };
}

function num2wordsOptions() {
  const mode = $("num2words-mode").value || "cardinal";
  return {
    mode,
    currency: mode === "currency" ? $("num2words-currency").value || null : null,
  };
}

function buildBatchPayload() {
  return {
    operation: state.operation,
    items: parseInputRows().map((row) => row.input),
    language: selectedLanguage(),
    tn_options: tnOptions(),
    itn_options: itnOptions(),
    num2words_options: num2wordsOptions(),
  };
}

function buildSinglePayload(input = firstInput()) {
  const language = selectedLanguage();
  if (state.operation === "tn") {
    return { text: input, language, options: tnOptions() };
  }
  if (state.operation === "itn") {
    return { text: input, language, options: itnOptions() };
  }
  return { number: input, language, options: num2wordsOptions() };
}

function parseInputRows() {
  return $("process-input")
    .value
    .split(/\r?\n/)
    .map((raw, index) => ({ lineNumber: index + 1, input: raw.trim() }))
    .filter((row) => row.input);
}

function firstInput() {
  return parseInputRows()[0]?.input || $("process-input").value.trim();
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail || response.statusText || `HTTP ${response.status}`;
    throw new Error(Array.isArray(detail) ? JSON.stringify(detail) : detail);
  }
  return data;
}

async function runBatch() {
  const rows = parseInputRows();
  if (rows.length === 0) {
    toast("请输入至少一行内容", true);
    return;
  }

  const payload = buildBatchPayload();
  setBusy("run-btn", true, "处理中");
  setStatus("处理中");
  setMeta("process-meta", "请求处理中");
  try {
    const result = await requestJson("/api/v1/batch", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    renderBatchResult(result, rows);
    setStatus("完成", result.error_count > 0);
  } catch (error) {
    clearResults();
    setStatus("失败", true);
    setMeta("process-meta", error.message, true);
    toast(error.message, true);
  } finally {
    setBusy("run-btn", false, "执行");
    updateApiPreview();
  }
}

function setBusy(id, busy, busyText) {
  const button = $(id);
  button.disabled = busy;
  button.setAttribute("aria-busy", String(busy));
  if (busy) {
    button.dataset.idleText = button.textContent;
    button.textContent = busyText;
  } else {
    button.textContent = button.dataset.idleText || button.textContent;
  }
}

function renderBatchResult(result, sourceRows) {
  const renderedRows = result.items.map((row) => ({
    ...row,
    lineNumber: sourceRows[row.index]?.lineNumber ?? row.index + 1,
  }));
  state.batchRows = renderedRows;
  $("process-output").value = renderedRows.map((row) => row.error ? "" : row.output).join("\n");
  $("copy-output-btn").disabled = false;
  $("copy-tsv-btn").disabled = false;
  $("result-detail").classList.remove("hidden");
  $("result-summary").textContent = `${result.success_count} 成功 / ${result.error_count} 失败`;
  setMeta("process-meta", `完成 ${result.items.length} 条 / 成功 ${result.success_count} 条，失败 ${result.error_count} 条 / 用时 ${result.metadata.elapsed_seconds ?? "-"}s`, result.error_count > 0);

  const table = $("result-table");
  table.innerHTML = "";
  for (const row of renderedRows) {
    const tr = document.createElement("tr");
    tr.classList.toggle("error-row", Boolean(row.error));
    tr.append(
      cell(String(row.lineNumber)),
      cell(row.input),
      cell(row.output || ""),
      cell(row.error || "", row.error ? "error-cell" : ""),
    );
    table.appendChild(tr);
  }
}

function cell(text, className = "") {
  const td = document.createElement("td");
  td.textContent = text;
  if (className) td.className = className;
  return td;
}

function clearResults() {
  state.batchRows = [];
  $("process-output").value = "";
  $("copy-output-btn").disabled = true;
  $("copy-tsv-btn").disabled = true;
  $("result-detail").classList.add("hidden");
  $("result-summary").textContent = "暂无结果";
  $("result-table").innerHTML = '<tr><td colspan="4" class="empty-cell">暂无结果</td></tr>';
  setMeta("process-meta", "等待处理");
}

function setMeta(id, text, isError = false) {
  const node = $(id);
  node.textContent = text;
  node.classList.toggle("is-error", isError);
}

function updateNum2WordsControls(preferredMode = null, preferredCurrency = null) {
  const language = selectedLanguage();
  const modesByLanguage = capabilities.operations?.num2words?.modes_by_language || {};
  const modes = modesByLanguage[language] || capabilities.operations?.num2words?.modes || {};
  const modeKeys = Object.keys(modes);
  const currentMode = preferredMode || $("num2words-mode").value;
  const selectedMode = Object.hasOwn(modes, currentMode)
    ? currentMode
    : modeKeys.includes("cardinal") ? "cardinal" : modeKeys[0] || "cardinal";
  fillSelect($("num2words-mode"), modes, selectedMode);

  const currencies = capabilities.operations?.num2words?.currencies_by_language?.[language] || [];
  const defaultsByLanguage = capabilities.operations?.num2words?.default_currency_by_language || {};
  const currentCurrency = preferredCurrency || $("num2words-currency").value;
  const selectedCurrency = currencies.includes(currentCurrency)
    ? currentCurrency
    : defaultsByLanguage[language] || currencies[0] || "";
  fillSelect($("num2words-currency"), Object.fromEntries(currencies.map((currency) => [currency, currency])), selectedCurrency);
  $("currency-field").classList.toggle("hidden", selectedMode !== "currency" || currencies.length === 0);
}

function syncLanguageScopedControls() {
  if (state.operation === "itn") {
    const options = capabilities.operations?.itn?.language_options?.[selectedLanguage()] || [];
    $("itn-standalone-number-field").classList.toggle("hidden", !options.includes("enable_standalone_number"));
    $("itn-zero-to-nine-field").classList.toggle("hidden", !options.includes("enable_0_to_9"));
  }
  if (state.operation === "num2words") {
    updateNum2WordsControls();
  }
}

async function loadExamples() {
  const version = encodeURIComponent(boot.assetVersion || "dev");
  try {
    const response = await fetch(`/static/data/examples.json?v=${version}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.examples = validateExamples(await response.json());
  } catch (error) {
    state.examples = [];
    renderExampleNotice(`示例读取失败：${error.message}`, true);
    return;
  }
  renderExamples();
}

function validateExamples(items) {
  const seen = new Set();
  if (!Array.isArray(items)) throw new Error("示例文件必须是数组");
  return items.map((example) => {
    if (!example.id || seen.has(example.id)) throw new Error("示例 id 缺失或重复");
    seen.add(example.id);
    if (!capabilities.operations?.[example.operation]) throw new Error(`示例任务不支持: ${example.operation}`);
    if (!capabilities.operations?.[example.operation]?.languages?.[example.language]) {
      throw new Error(`示例语言不支持: ${example.language}`);
    }
    return example;
  });
}

function renderExamples() {
  const list = $("example-list");
  list.innerHTML = "";
  const examples = state.exampleFilter === "all"
    ? state.examples
    : state.examples.filter((example) => example.operation === state.exampleFilter);
  if (examples.length === 0) {
    renderExampleNotice("当前筛选条件下没有示例");
    return;
  }
  for (const example of examples) {
    list.appendChild(exampleNode(example));
  }
}

function renderExampleNotice(message, isError = false) {
  const list = $("example-list");
  list.innerHTML = "";
  const item = document.createElement("article");
  item.className = "example-notice";
  item.classList.toggle("is-error", isError);
  item.textContent = message;
  list.appendChild(item);
}

function exampleNode(example) {
  const item = document.createElement("article");
  item.className = "example-item";

  const head = document.createElement("div");
  head.className = "example-head";

  const titleGroup = document.createElement("div");
  titleGroup.className = "example-title-group";
  const title = document.createElement("h3");
  title.textContent = example.title;
  const meta = document.createElement("div");
  meta.className = "example-meta";
  meta.append(
    badge(operationLabel(example.operation)),
    badge(languageLabel(example.language, example.operation)),
    badge(example.scenario),
  );
  titleGroup.append(title, meta);

  const actions = document.createElement("div");
  actions.className = "example-actions";
  const applyButton = document.createElement("button");
  applyButton.className = "btn btn-secondary";
  applyButton.type = "button";
  applyButton.textContent = "套用";
  applyButton.addEventListener("click", () => applyExample(example, false));
  const runButton = document.createElement("button");
  runButton.className = "btn btn-primary";
  runButton.type = "button";
  runButton.textContent = "套用并执行";
  runButton.addEventListener("click", () => applyExample(example, true));
  actions.append(applyButton, runButton);
  head.append(titleGroup, actions);

  const io = document.createElement("div");
  io.className = "example-io";
  io.append(exampleBlock("输入", example.input), exampleBlock("效果", example.expected));

  item.append(head, io);
  return item;
}

function badge(text) {
  const node = document.createElement("span");
  node.className = "example-badge";
  node.textContent = text;
  return node;
}

function exampleBlock(label, text) {
  const box = document.createElement("div");
  box.className = "example-box";
  const title = document.createElement("strong");
  title.textContent = label;
  const pre = document.createElement("pre");
  pre.textContent = text;
  box.append(title, pre);
  return box;
}

async function applyExample(example, shouldRun) {
  setOperation(example.operation, true);
  setLanguage(example.language);
  applyExampleOptions(example);
  $("process-input").value = example.input;
  clearResults();
  setView("process");
  if (shouldRun) await runBatch();
}

function setLanguage(language) {
  const select = $("language-select");
  if ([...select.options].some((option) => option.value === language)) {
    select.value = language;
  }
  syncLanguageScopedControls();
}

function applyExampleOptions(example) {
  const options = example.options || {};
  if (example.operation === "tn") {
    $("input-case-select").value = options.input_case || "cased";
    $("tn-deterministic").checked = options.deterministic ?? true;
    $("tn-post-process").checked = options.post_process ?? true;
    $("tn-punct-pre").checked = options.punct_pre_process ?? false;
    $("tn-punct-post").checked = options.punct_post_process ?? false;
    $("tn-batch-size").value = options.batch_size || 1;
    $("tn-n-jobs").value = options.n_jobs || 1;
    $("tn-whitelist").value = options.whitelist_path || "";
  } else if (example.operation === "itn") {
    $("itn-standalone-number").checked = options.enable_standalone_number ?? true;
    $("itn-zero-to-nine").checked = options.enable_0_to_9 ?? true;
  } else {
    updateNum2WordsControls(options.mode, options.currency);
  }
}

function setExampleFilter(filter) {
  state.exampleFilter = filter;
  document.querySelectorAll("[data-example-filter]").forEach((button) => {
    const active = button.dataset.exampleFilter === filter;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  renderExamples();
}

function apiSamplePayload(operation) {
  if (operation === "capabilities") return null;
  if (operation === "batch") {
    return {
      operation: state.operation,
      items: parseInputRows().map((row) => row.input),
      language: selectedLanguage(),
      tn_options: tnOptions(),
      itn_options: itnOptions(),
      num2words_options: num2wordsOptions(),
    };
  }
  return buildSinglePayload();
}

function updateApiPreview(payload = apiSamplePayload($("api-operation-select").value)) {
  const operation = $("api-operation-select").value;
  const definition = endpointMap[operation];
  $("api-endpoint-text").textContent = `${definition.method} ${definition.url}`;
  const editor = $("api-request-json");
  const isGet = definition.method === "GET";
  editor.disabled = isGet;
  editor.classList.toggle("is-note", isGet);
  editor.value = isGet ? "GET 接口无需请求体" : formatJson(payload);
  $("api-copy-request-btn").disabled = isGet;
  $("api-curl-command").textContent = curlFor(definition, payload);
}

function updateApiCurlFromEditor() {
  const operation = $("api-operation-select").value;
  const definition = endpointMap[operation];
  $("api-curl-command").textContent = curlFor(definition, parseApiEditorPayload());
}

function parseApiEditorPayload() {
  const definition = endpointMap[$("api-operation-select").value];
  if (definition.method === "GET") return null;
  const raw = $("api-request-json").value.trim();
  if (!raw) return {};
  return JSON.parse(raw);
}

function curlFor(definition, payload) {
  const url = new URL(definition.url, window.location.origin).toString();
  if (definition.method === "GET") return `curl -s ${shellQuote(url)}`;
  return `curl -s -X ${definition.method} ${shellQuote(url)} -H 'Content-Type: application/json' -d ${shellQuote(JSON.stringify(payload))}`;
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, "'\\''")}'`;
}

async function runApiRequest() {
  const operation = $("api-operation-select").value;
  const definition = endpointMap[operation];
  let payload = null;
  try {
    payload = parseApiEditorPayload();
  } catch (error) {
    setApiResponse(`请求 JSON 无效：${error.message}`, true);
    return;
  }

  setBusy("api-run-btn", true, "调用中");
  setMeta("api-meta", "请求发送中");
  try {
    const options = definition.method === "GET"
      ? {}
      : { method: definition.method, body: JSON.stringify(payload) };
    const result = await requestJson(definition.url, options);
    setApiResponse(formatJson(result), false);
    setMeta("api-meta", "请求完成");
  } catch (error) {
    setApiResponse(error.message, true);
    setMeta("api-meta", "请求失败", true);
  } finally {
    setBusy("api-run-btn", false, "执行调用");
  }
}

function setApiResponse(text, isError) {
  const node = $("api-response-json");
  node.textContent = text;
  node.classList.toggle("is-error", isError);
}

function formatJson(value) {
  return JSON.stringify(value, null, 2);
}

async function copyText(text, successMessage) {
  if (!text) {
    toast("没有可复制的内容", true);
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
    toast(successMessage);
  } catch {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
    toast(successMessage);
  }
}

function batchOutputText() {
  return state.batchRows.map((row) => row.error ? "" : row.output).join("\n");
}

function batchTsv() {
  const rows = [["line", "input", "output", "error"], ...state.batchRows.map((row) => [
    row.lineNumber,
    row.input,
    row.output || "",
    row.error || "",
  ])];
  return rows.map((row) => row.map((cellValue) => String(cellValue).replace(/\t/g, " ").replace(/\r?\n/g, " ")).join("\t")).join("\n");
}

async function refreshCapabilities() {
  try {
    capabilities = await requestJson("/api/v1/capabilities");
  } catch {
    capabilities = boot.capabilities || { operations: {} };
  }
}

function wireEvents() {
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => setView(button.dataset.view));
  });
  document.querySelectorAll("[data-example-filter]").forEach((button) => {
    button.addEventListener("click", () => setExampleFilter(button.dataset.exampleFilter));
  });
  $("operation-select").addEventListener("change", () => setOperation($("operation-select").value));
  $("language-select").addEventListener("change", () => {
    syncLanguageScopedControls();
    clearResults();
    updateApiPreview();
  });
  $("num2words-mode").addEventListener("change", () => {
    updateNum2WordsControls($("num2words-mode").value);
    clearResults();
    updateApiPreview();
  });
  document.querySelectorAll("#tn-options input, #tn-options select, #itn-options input, #itn-options select, #num2words-options select").forEach((control) => {
    if (control.id === "num2words-mode") return;
    control.addEventListener("change", () => {
      clearResults();
      updateApiPreview();
    });
  });
  $("process-input").addEventListener("input", () => {
    clearResults();
    updateApiPreview();
  });
  $("run-btn").addEventListener("click", runBatch);
  $("clear-btn").addEventListener("click", () => {
    $("process-input").value = "";
    clearResults();
    updateApiPreview();
  });
  $("sample-btn").addEventListener("click", () => setOperation(state.operation));
  $("copy-output-btn").addEventListener("click", () => copyText(batchOutputText(), "已复制输出"));
  $("copy-tsv-btn").addEventListener("click", () => copyText(batchTsv(), "已复制 TSV"));
  $("api-operation-select").addEventListener("change", () => updateApiPreview());
  $("api-request-json").addEventListener("input", () => {
    try {
      updateApiCurlFromEditor();
      setMeta("api-meta", "请求已编辑，等待执行");
    } catch {
      setMeta("api-meta", "请求 JSON 无效", true);
    }
  });
  $("api-sample-btn").addEventListener("click", () => updateApiPreview());
  $("api-import-btn").addEventListener("click", () => {
    $("api-operation-select").value = parseInputRows().length > 1 ? "batch" : state.operation;
    updateApiPreview();
  });
  $("api-copy-request-btn").addEventListener("click", () => copyText($("api-request-json").value, "已复制请求 JSON"));
  $("api-copy-curl-btn").addEventListener("click", () => copyText($("api-curl-command").textContent, "已复制 curl"));
  $("api-run-btn").addEventListener("click", runApiRequest);
  $("api-clear-response-btn").addEventListener("click", () => {
    setApiResponse("等待执行", false);
    setMeta("api-meta", "未发送请求");
  });
}

async function init() {
  await refreshCapabilities();
  wireEvents();
  setOperation("tn");
  updateApiPreview();
  await loadExamples();
  setStatus("就绪");
}

init();
