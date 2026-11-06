from services.location_service import LocationService

# Create an instance of LocationService

location_service = LocationService()

# Ask the user to enter a location

city_name = input("Enter a city or location: ")

# Search for the entered location

results = location_service.search_location(city_name)

# Display matching locations

if results:

    print("\nLOCATION SEARCH SUCCESSFUL!")

    for index, location in enumerate(results, start=1):

        print(f"\nLocation {index}")

        print("------------------------------")

        print("Name:", location["name"])

        print("Country:", location["country"])

        print("Latitude:", location["latitude"])

        print("Longitude:", location["longitude"])

        print("Timezone:", location["timezone"])

else:

    print("No matching location found.")
