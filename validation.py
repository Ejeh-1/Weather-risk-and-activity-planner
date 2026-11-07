import re
from datetime import datetime


class InputValidator:

    # Clean user input
    def clean_input(self, user_input):

        if not isinstance(user_input, str):
            raise ValueError("Input must be text")

        return user_input.strip()


    # Handle errors consistently
    def handle_errors(self, user_input):

        try:
            user_input = self.clean_input(user_input)

            if not user_input:
                raise ValueError("Input cannot be empty")

            return user_input

        except ValueError as error:
            return str(error)


    # Validate location
    def validate_location(self, location):

        location = self.handle_errors(location)

        if location == "Input cannot be empty" or location == "Input must be text":
            return False

        pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,'-]+$"

        if not re.fullmatch(pattern, location):
            return False

        if not re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]", location):
            return False

        return True


    # Validate date
    def validate_date(self, date):

        date = self.handle_errors(date)

        if date == "Input cannot be empty" or date == "Input must be text":
            return False

        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                return False

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

        time = self.handle_errors(time)

        if time == "Input cannot be empty" or time == "Input must be text":
            return False

        try:
            if not re.fullmatch(r"\d{2}:\d{2}", time):
                return False

            datetime.strptime(time, "%H:%M")

            return True

        except ValueError:
            return False