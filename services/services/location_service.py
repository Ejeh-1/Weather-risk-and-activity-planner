import requests

class LocationService:

    """Handles searching for locations and retrieving their coordinates."""

    def __init__(self):

        # Open-Meteo Geocoding API endpoint

        self.base_url = "https://geocoding-api.open-meteo.com/v1/search"

    def search_location(self, city_name, country_code=None):

        """

        Search for a city, optionally filtering by country code.

        Args:

            city_name: Name of the city.

            country_code: Optional two-letter country code.

        Returns:

            A list of matching locations.

        """

        # Validate the city name

        if not city_name or not city_name.strip():

            return []

        # Validate the country code if provided

        if country_code:

            country_code = country_code.strip().upper()

            if len(country_code) != 2 or not country_code.isalpha():

                return []

        # Prepare API request parameters

        params = {

            "name": city_name.strip(),

            "count": 10,

            "language": "en",

            "format": "json"

        }

        # Add country filter when provided

        if country_code:

            params["countryCode"] = country_code

        try:

            # Send request to the Geocoding API

            response = requests.get(

                self.base_url,

                params=params,

                timeout=10

            )

            # Check for HTTP errors

            response.raise_for_status()

            # Convert response into a dictionary

            data = response.json()

            # Extract matching locations

            locations = data.get("results", [])

            # Return relevant location information

            return [

                {

                    "name": location["name"],

                    "country": location.get("country"),

                    "latitude": location["latitude"],

                    "longitude": location["longitude"],

                    "timezone": location.get("timezone")

                }

                for location in locations

            ]

        except requests.exceptions.RequestException as e:

            # Handle API connection errors

            print(f"Location API error: {e}")

            return []
