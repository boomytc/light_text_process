from __future__ import annotations

import importlib.util
import io
from pathlib import Path
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
    def test_status_reports_vendor_free_cache_policy(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = cache_maintenance.main(["status"])

        self.assertEqual(exit_code, 0)
        self.assertIn("cache_policy: none", output.getvalue())
        self.assertIn("vendor grammar caches are not used", output.getvalue())


if __name__ == "__main__":
    unittest.main()
