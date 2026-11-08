class InvalidInputError(Exception):

    """Raised when a user's input is invalid."""

    pass

class WeatherDataError(Exception):

    """Raised when weather data is unavailable or unusable."""

    pass

class LocationServiceError(WeatherDataError):

    """Raised when the location service cannot be reached or fails."""

    pass
