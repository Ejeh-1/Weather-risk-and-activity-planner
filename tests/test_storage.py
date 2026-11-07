import json
import tempfile
import unittest
from pathlib import Path
from managers.storage import StorageManager, StorageError


class StorageManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.storage = StorageManager(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_search_history_saves_and_returns_newest_first(self):
        self.storage.save_search("Abuja", "Jogging")
        self.storage.save_search("Lagos", "Football")
        history = self.storage.get_search_history()
        self.assertEqual([item["location"] for item in history], ["Lagos", "Abuja"])

    def test_favourites_prevent_duplicates_and_can_be_removed(self):
        self.assertTrue(self.storage.add_favourite("Abuja"))
        self.assertFalse(self.storage.add_favourite("abuja"))
        self.assertTrue(self.storage.remove_favourite("ABUJA"))
        self.assertEqual(self.storage.get_favourites(), [])

    def test_activity_plan_is_saved(self):
        saved = self.storage.save_activity_plan({"activity": "Picnic", "location": "Abuja"})
        self.assertEqual(saved["plan"]["activity"], "Picnic")
        self.assertEqual(len(self.storage.get_activity_plans()), 1)

    def test_missing_files_return_empty_lists(self):
        self.assertEqual(self.storage.get_search_history(), [])
        self.assertEqual(self.storage.get_favourites(), [])
        self.assertEqual(self.storage.get_activity_plans(), [])

    def test_corrupt_json_raises_clear_error(self):
        self.storage.history_file.write_text("{broken", encoding="utf-8")
        with self.assertRaises(StorageError):
            self.storage.get_search_history()


if __name__ == "__main__":
    unittest.main()
