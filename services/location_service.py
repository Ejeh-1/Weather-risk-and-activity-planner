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

        if not isinstance(city_name, str):
            return []

        city_name = city_name.strp()
        if not city_name:
            return []
            

        # Validate the country code if provided

        if country_code is not None:
            
            if not isinstance(country_code, str):
                return []

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

            # Convert API response

            try:
                data = response.json()

            except ValueError:
                print("Location API error: Invalid JSON response")
                return []
                
                

            # Ensure the API response is a dictionary

            if not isinstance(data, dict):
                return []

            

            # Extract matching locations

            locations = data.get("results", [])

            # Ensure results contain a list

            if not isinstance(locations, list):
                return []

              

            # Return relevant location information

            valid_location = []

            for location in locations:

                if not isinstance(location, dict):
                    continue

                # Check for require fields
                required_field = ["name", "latitude", "longitude"]

                if not all(field in location for field in required_fields):
                    continue

                # Ensure coordinates are valid numbers

                latitude = location["latitude"]

                longitude = location["longitude"]

                if not isinstance(latitude, (int, float)):

                    continue

                if not isinstance(longitude, (int, float)):

                    continue

                # Check coordinate ranges

                if not -90 <= latitude <= 90:

                    continue

                if not -180 <= longitude <= 180:

                    continue

                valid_locations.append({
                    "name": location["name"],
                    "country": location.get("country"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "timezone": location.get("timezone")
                })
            return valid_locations
            
 

        except requests.exceptions.RequestException as e:

            # Handle API connection errors

            print(f"Location API error: {e}")

            return []
