import unittest
from datetime import datetime, timedelta

from validation import InputValidator


class TestInputValidator(unittest.TestCase):

    def setUp(self):
        self.validator = InputValidator()

    # Test empty inputs
    def test_empty_location(self):
        self.assertFalse(
            self.validator.validate_location("")
        )

    def test_empty_date(self):
        self.assertFalse(
            self.validator.validate_date("")
        )

    def test_empty_time(self):
        self.assertFalse(
            self.validator.validate_time("")
        )

    # Test invalid dates
    def test_invalid_date(self):
        self.assertFalse(
            self.validator.validate_date("2026-15-40")
        )

    def test_wrong_date_format(self):
        self.assertFalse(
            self.validator.validate_date("07/11/2026")
        )

    # Test past dates
    def test_past_date(self):
        yesterday = (
            datetime.today().date() - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        self.assertFalse(
            self.validator.validate_date(yesterday)
        )

    def test_future_date(self):
        tomorrow = (
            datetime.today().date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        self.assertTrue(
            self.validator.validate_date(tomorrow)
        )

    # Test invalid time formats
    def test_invalid_time(self):
        self.assertFalse(
            self.validator.validate_time("25:90")
        )

    def test_wrong_time_format(self):
        self.assertFalse(
            self.validator.validate_time("9:30 AM")
        )

    def test_valid_time(self):
        self.assertTrue(
            self.validator.validate_time("14:30")
        )

    # Test handle_errors()
    def test_handle_errors_valid_input(self):
        self.assertEqual(
            self.validator.handle_errors(" Abuja "),
            "Abuja"
        )

    def test_handle_errors_empty_input(self):
        self.assertEqual(
            self.validator.handle_errors(""),
            "Input cannot be empty"
        )

    def test_handle_errors_spaces_only(self):
        self.assertEqual(
            self.validator.handle_errors("   "),
            "Input cannot be empty"
        )


if __name__ == "__main__":
    unittest.main()