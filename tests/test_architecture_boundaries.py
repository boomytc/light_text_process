from __future__ import annotations

from pathlib import Path
import re
import unittest


PROJECT_DIR = Path(__file__).resolve().parents[1]
VENDOR_MODULE = "_".join(("fun", "text", "processing"))
RULE_BUCKET_IMPORT_PATTERNS = (
    re.compile(r"(?m)^\s*(?:from\s+light_text_process\.rules\s+import\s+.*\ben\b|import\s+light_text_process\.rules\.en\b)"),
    re.compile(r"(?m)^\s*(?:from\s+light_text_process\.rules\s+import\s+.*\bzh\b|import\s+light_text_process\.rules\.zh\b)"),
)


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_internal_compatibility_facades_are_not_present(self) -> None:
        self.assertFalse((PROJECT_DIR / "light_text_process" / "rules" / "_shared.py").exists())
        self.assertFalse((PROJECT_DIR / "light_text_process" / "rules" / "en.py").exists())
        self.assertFalse((PROJECT_DIR / "light_text_process" / "rules" / "zh.py").exists())
        self.assertFalse((PROJECT_DIR / "light_text_process" / "rules" / "pipeline_dispatch.py").exists())

    def test_focused_rule_modules_do_not_import_rule_buckets_or_runtime_backend(self) -> None:
        for path in (PROJECT_DIR / "light_text_process" / "rules").glob("*.py"):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn(VENDOR_MODULE, source, path.name)
            self.assertNotIn("light_text_process.rules._shared", source, path.name)
            self.assertNotIn("light_text_process.rules.pipeline_dispatch", source, path.name)
            for pattern in RULE_BUCKET_IMPORT_PATTERNS:
                self.assertIsNone(pattern.search(source), path.name)

    def test_vendor_backend_imports_are_not_present(self) -> None:
        self.assertFalse((PROJECT_DIR / "light_text_process" / "runtime" / f"{VENDOR_MODULE}.py").exists())
        for path in (PROJECT_DIR / "light_text_process").rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn(f"from {VENDOR_MODULE}", source, str(path))
            self.assertNotIn(f"import {VENDOR_MODULE}", source, str(path))


if __name__ == "__main__":
    unittest.main()
