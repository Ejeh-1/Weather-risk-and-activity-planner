import re
from datetime import datetime


class InputValidator:

    def clean_input(self, user_input):
        return user_input.strip()

    def validate_location(self, location):
        location = self.clean_input(location)

        if not location:
            return False

        pattern = r"^[a-zA-Z\s'-]+$"

        if re.fullmatch(pattern, location):
            return True
        else:
            return False

    def validate_date(self, date):
        try:
            date = self.clean_input(date)

            selected_date = datetime.strptime(date, "%Y-%m-%d").date()

            if selected_date < datetime.today().date():
                return False

            return True

        except ValueError:
            return False

    def validate_time(self, time):
        try:
            time = self.clean_input(time)

            datetime.strptime(time, "%H:%M")

            return True

        except ValueError:
            return False

    def handle_errors(self, user_input):
        try:
            if not user_input:
                raise ValueError("Input cannot be empty")

            return self.clean_input(user_input)

        except ValueError as error:
            return str(error)
