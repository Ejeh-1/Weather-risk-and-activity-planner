from services.location_service import LocationService

# Create an instance of LocationService

location_service = LocationService()

# Ask the user for a city and country code

city_name = input("Enter a city: ")

country_code = input("Enter country code (e.g. NG, GB, US): ")

# Search for the city within the specified country

results = location_service.search_location(

    city_name,

    country_code

)

# Display matching locations

if results:

    print("\nLOCATION SEARCH SUCCESSFUL!")

    for index, location in enumerate(results, start=1):

        print(f"\nLocation {index}")

        print("-" * 40)

        print("Name:", location["name"])

        print("Country:", location["country"])

        print("Latitude:", location["latitude"])

        print("Longitude:", location["longitude"])

        print("Timezone:", location["timezone"])

else:

    print("No matching location found.")
