from __future__ import annotations

import asyncio
import unittest

from api.routes import health, router
from app import create_app


class ProductScaffoldTests(unittest.TestCase):
    def test_app_can_be_created(self) -> None:
        app = create_app()

        self.assertEqual(app.title, "Light Text Process Web")

    def test_health_endpoint(self) -> None:
        response = asyncio.run(health())

        self.assertEqual(response, {"status": "ok"})

    def test_scaffold_routes_are_registered(self) -> None:
        app = create_app()
        paths = _route_paths(app.routes)

        self.assertIn("/", paths)
        self.assertIn("/static", paths)
        self.assertIn("/health", _route_paths(router.routes))


def _route_paths(routes: object) -> set[str]:
    paths: set[str] = set()
    for route in routes:
        path = getattr(route, "path", None)
        if isinstance(path, str):
            paths.add(path)
        child_routes = getattr(route, "routes", None)
        if child_routes is not None:
            paths.update(_route_paths(child_routes))
    return paths


if __name__ == "__main__":
    unittest.main()
