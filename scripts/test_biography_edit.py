import reflex as rx
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.states import research_state as research


class BiographyEditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "test.db"
        self.patch = patch.object(research, "DB_PATH", self.path)
        self.patch.start()
        self.values = {
            "nationality": "Brasil",
            "birth_date": "1900-01-02",
            "death_date": "1980-03-04",
            "birth_place": "Rio",
            "death_place": "São Paulo",
        }
        with sqlite3.connect(self.path) as conn:
            conn.execute("""CREATE TABLE people (
                id TEXT PRIMARY KEY, name TEXT, nationality TEXT, birth_date TEXT,
                death_date TEXT, birth_place TEXT, death_place TEXT,
                birth_lat REAL, birth_lng REAL, death_lat REAL, death_lng REAL,
                completeness INTEGER, is_living INTEGER,
                article_title TEXT, summary TEXT, metadata TEXT)""")
            conn.execute(
                "INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "Q1",
                    "Pessoa",
                    *self.values.values(),
                    1,
                    2,
                    3,
                    4,
                    100,
                    0,
                    "Artigo original",
                    "Resumo original",
                    "Preservar",
                ),
            )

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def row(self):
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            return dict(
                conn.execute(
                    "SELECT * FROM people WHERE id = ?", ("Q1",)
                ).fetchone()
            )

    def test_normalization(self):
        cases = {
            "29/02/2000": "2000-02-29",
            "02/1900": "1900-02",
            "44 a.C.": "-0044",
            "-0044-03-15": "-0044-03-15",
            "1900": "1900",
            "—": "—",
            " ": "—",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(
                    research._normalize_edit_date(value, "Data"), expected
                )
        for value in (
            "29/02/1900",
            "31/04/2000",
            "2000-13-02",
            "ontem",
            "0000",
            "2020-00-05",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                research._normalize_edit_date(value, "Data")
        self.assertEqual(research._stored_year("-0044-03-15"), -44)

    def test_chronology(self):
        for birth, death in (
            ("1901", "1900"),
            ("02/01/1900", "01/01/1900"),
            ("44 a.C.", "45 a.C."),
        ):
            with self.subTest(birth=birth), self.assertRaises(ValueError):
                research._validate_biography_edit(
                    {**self.values, "birth_date": birth, "death_date": death}
                )
        research._validate_biography_edit(
            {**self.values, "birth_date": "1900", "death_date": "01/01/1900"}
        )

    def test_update_preserves_uneditable_fields_and_other_coordinates(self):
        before = self.row()
        result = research.update_biography_db(
            "Q1",
            {
                **self.values,
                "birth_place": "  Lisboa  ",
                "nationality": "Portugal",
            },
            self.values,
        )
        after = self.row()
        self.assertEqual(after["birth_place"], "Lisboa")
        self.assertEqual((after["birth_lat"], after["birth_lng"]), (0, 0))
        self.assertEqual((after["death_lat"], after["death_lng"]), (3, 4))
        for field in ("id", "name", "article_title", "summary", "metadata"):
            self.assertEqual(after[field], before[field])
        self.assertEqual(result["nationality"], after["nationality"])

    def test_missing_conflicting_and_invalid_rows_do_not_write(self):
        before = self.row()
        with self.assertRaises(ValueError):
            research.update_biography_db("missing", self.values, self.values)
        with self.assertRaises(ValueError):
            research.update_biography_db(
                "Q1", self.values, {**self.values, "nationality": "Outra"}
            )
        with self.assertRaises(ValueError):
            research.update_biography_db(
                "Q1", {**self.values, "death_date": "ontem"}, self.values
            )
        self.assertEqual(before, self.row())

    def test_write_failure_is_raised_and_rolled_back(self):
        before = self.row()
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "CREATE TRIGGER reject_edit BEFORE UPDATE ON people BEGIN SELECT RAISE(ABORT, 'blocked'); END"
            )
        with self.assertRaises(sqlite3.DatabaseError):
            research.update_biography_db(
                "Q1", {**self.values, "nationality": "Portugal"}, self.values
            )
        self.assertEqual(before, self.row())

    def test_living_status_and_completeness(self):
        result = research.update_biography_db(
            "Q1",
            {**self.values, "death_date": "Vivo(a)", "death_place": "—"},
            self.values,
        )
        self.assertTrue(result["is_living"])
        expected = {key: result[key] for key in self.values}
        result = research.update_biography_db(
            "Q1",
            {**expected, "death_date": "2020", "nationality": ""},
            expected,
        )
        self.assertFalse(result["is_living"])
        self.assertEqual(result["nationality"], "—")
        self.assertEqual(self.row()["death_date"], "2020")
        self.assertEqual(result["completeness"], 67)


if __name__ == "__main__":
    unittest.main()
