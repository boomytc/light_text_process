from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout


PROJECT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_DIR / "scripts" / "cache_maintenance.py"


def load_cache_maintenance_module():
    spec = importlib.util.spec_from_file_location("cache_maintenance", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cache_maintenance.py cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cache_maintenance = load_cache_maintenance_module()


class CacheMaintenanceTests(unittest.TestCase):
    def test_cache_selection_by_operation_and_language(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            for name in (
                "zh_tn_True_deterministic_cased__tokenize.far",
                "zh_tn_True_deterministic_verbalizer.far",
                "_zh_itn.far",
                "_ja_itn_standalone_0_zero_to_nine_0.far",
                "notes.txt",
            ):
                (cache_dir / name).write_text("cache", encoding="utf-8")

            zh_files = cache_maintenance.selected_cache_files(
                cache_dir=cache_dir,
                profiles=None,
                include_all=False,
                operation=None,
                language="zh",
            )
            tn_files = cache_maintenance.selected_cache_files(
                cache_dir=cache_dir,
                profiles=None,
                include_all=False,
                operation="tn",
                language=None,
            )

        self.assertEqual([path.name for path in zh_files], [
            "_zh_itn.far",
            "zh_tn_True_deterministic_cased__tokenize.far",
            "zh_tn_True_deterministic_verbalizer.far",
        ])
        self.assertEqual([path.name for path in tn_files], [
            "zh_tn_True_deterministic_cased__tokenize.far",
            "zh_tn_True_deterministic_verbalizer.far",
        ])

    def test_clear_requires_explicit_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "provide --profile"):
                cache_maintenance.selected_cache_files(
                    cache_dir=Path(temp_dir),
                    profiles=None,
                    include_all=False,
                    operation=None,
                    language=None,
                )

    def test_delete_targets_is_dry_run_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "_zh_itn.far"
            target.write_text("cache", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                cache_maintenance.delete_targets([target], dry_run=True)

            self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
