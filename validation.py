import re
from datetime import datetime


class InputValidator:

    # Clean user input
    def clean_input(self, user_input):

        if not isinstance(user_input, str):
            raise ValueError("Input must be text")

        return user_input.strip()


    # Validate location
    def validate_location(self, location):

        try:
            location = self.clean_input(location)

            if not location:
                return False

            pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,'-]+$"

            if not re.fullmatch(pattern, location):
                return False

            if not re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]", location):
                return False

            return True

        except ValueError:
            return False


    # Validate date
    def validate_date(self, date):

        try:
            date = self.clean_input(date)

            selected_date = datetime.strptime(
                date, "%Y-%m-%d"
            ).date()

            if selected_date < datetime.today().date():
                return False

            return True

        except ValueError:
            return False


    # Validate time
    def validate_time(self, time):

        try:
            time = self.clean_input(time)

            datetime.strptime(time, "%H:%M")

            return True

        except ValueError:
            return False


    # Handle errors
    def handle_errors(self, user_input):

        try:
            user_input = self.clean_input(user_input)

            if not user_input:
                raise ValueError("Input cannot be empty")

            return user_input

        except ValueError as error:
            return str(error)
