import requests  # Allows us to make HTTP requests to the Geocoding API

class LocationService:

    """Handles searching for locations and retrieving their coordinates."""

    def __init__(self):

        # Open-Meteo Geocoding API endpoint

        self.base_url = "https://geocoding-api.open-meteo.com/v1/search"

    def search_location(self, city_name):

        """

        Search for a city and return its location details.

        Args:

            city_name: The name of the city entered by the user.

        Returns:

            A list containing matching locations and their coordinates.

        """

        # Check whether the user entered an empty location

        if not city_name or not city_name.strip():

            return []

        # Parameters sent to the Geocoding API

        params = {

            "name": city_name.strip(),  # Remove unnecessary spaces

            "count": 5,                 # Return a maximum of 5 matches

            "language": "en",           # Return results in English

            "format": "json"            # Request JSON response

        }

        try:

            # Send a GET request to the Geocoding API

            response = requests.get(

                self.base_url,

                params=params,

                timeout=10

            )

            # Raise an exception if the request was unsuccessful

            response.raise_for_status()

            # Convert the API response into a Python dictionary

            data = response.json()

            # Extract the matching locations from the response

            locations = data.get("results", [])

            # Return only the location details our application needs

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

        except requests.exceptions.RequestException as error:

            # Display an error if the API request fails

            print(f"Location API error: {error}")

            # Return an empty list when no results can be retrieved

            return []
