import reflex as rx
import math
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.states import research_state as research


class DistanceTests(unittest.TestCase):
    def test_known_city_displacements(self):
        einstein = research.haversine_distance_km(
            48.4011, 9.9876, 40.3573, -74.6672
        )
        curie = research.haversine_distance_km(
            52.2297, 21.0122, 45.9236, 6.6950
        )
        self.assertTrue(6300 < einstein < 6600)
        self.assertTrue(1200 < curie < 1300)
        self.assertEqual(research.format_distance_km(6420.45), "6.420,4 km")

    def test_missing_invalid_and_living(self):
        for lat, lng in (
            (0, 0),
            (91, 1),
            (-91, 1),
            (1, 181),
            (1, -181),
            (math.nan, 1),
            (1, math.inf),
        ):
            self.assertIsNone(research.haversine_distance_km(lat, lng, 40, 20))
            self.assertIsNone(research.haversine_distance_km(40, 20, lat, lng))
        self.assertIsNone(research.haversine_distance_km(40, 20, 41, 21, True))
        self.assertIsNotNone(research.haversine_distance_km(0, 10, 10, 0))

    def test_zero_near_identical_antipodal_and_antimeridian(self):
        self.assertEqual(research.haversine_distance_km(40, 20, 40, 20), 0)
        self.assertLess(
            research.haversine_distance_km(40, 20, 40.0001, 20.0001), 0.02
        )
        self.assertAlmostEqual(
            research.haversine_distance_km(0, 90, 0, -90),
            math.pi * 6371.0088,
            places=5,
        )
        self.assertLess(
            research.haversine_distance_km(10, 179.9, 10, -179.9), 23
        )


class DemoSeedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "geohist.db"
        self.patch = patch.object(research, "DB_PATH", self.path)
        self.patch.start()
        research.init_db()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_seed_refresh_delete_and_no_history(self):
        self.assertEqual(research.seed_demo_biographies(self.path), 2)
        first = research.load_people_db()
        self.assertEqual(research.seed_demo_biographies(self.path), 0)
        self.assertEqual(first, research.load_people_db())
        self.assertEqual(research.load_history_db(), [])
        for person in first:
            self.assertEqual(person["description"], research.DEMO_LABEL)
            self.assertEqual(person["searched_at"], "")
            self.assertTrue(
                person["article_url"].startswith(
                    "https://pt.wikipedia.org/wiki/"
                )
            )
        research.delete_person_db("Q937")
        self.assertEqual(research.seed_demo_biographies(self.path), 0)
        self.assertEqual(len(research.load_people_db()), 1)

    def test_existing_records_and_corrections_preserved(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "INSERT INTO people (id, name, birth_place, birth_lat) VALUES (?, ?, ?, ?)",
                ("Q937", "Correção existente", "Local corrigido", 12.34),
            )
            conn.execute(
                "INSERT INTO people (id, name) VALUES (?, ?)",
                ("Q42", "Outro registro"),
            )
            before = conn.execute(
                "SELECT * FROM people WHERE id='Q937'"
            ).fetchone()
        self.assertEqual(research.seed_demo_biographies(self.path), 1)
        with sqlite3.connect(self.path) as conn:
            self.assertEqual(
                before,
                conn.execute("SELECT * FROM people WHERE id='Q937'").fetchone(),
            )
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM people").fetchone()[0], 3
            )
        self.assertEqual(research.seed_demo_biographies(self.path), 0)

    def test_failed_seed_rolls_back_marker_and_rows(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "CREATE TRIGGER reject_demo BEFORE INSERT ON people WHEN NEW.id='Q7186' BEGIN SELECT RAISE(ABORT, 'blocked'); END"
            )
        with self.assertRaises(sqlite3.DatabaseError):
            research.seed_demo_biographies(self.path)
        with sqlite3.connect(self.path) as conn:
            self.assertEqual(
                conn.execute("PRAGMA application_id").fetchone()[0], 0
            )
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM people").fetchone()[0], 0
            )
            conn.execute("DROP TRIGGER reject_demo")
        self.assertEqual(research.seed_demo_biographies(self.path), 2)


if __name__ == "__main__":
    unittest.main()
