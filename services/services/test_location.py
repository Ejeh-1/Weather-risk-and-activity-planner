from services.location_service import LocationService

# Create an instance of the LocationService class

location_service = LocationService()

# Search for Abuja

results = location_service.search_location("Abuja")

# Check whether any locations were found

if results:

    print("\nLOCATION SEARCH SUCCESSFUL!")

    # Display the details of each matching location

    for location in results:

        print("------------------------------")

        print("Name:", location["name"])

        print("Country:", location["country"])

        print("Latitude:", location["latitude"])

        print("Longitude:", location["longitude"])

        print("Timezone:", location["timezone"])

else:

    print("No location found.")
