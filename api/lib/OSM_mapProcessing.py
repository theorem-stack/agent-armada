import requests

def fetch_buildings_in_bounding_box(bbox):
    # Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Define an Overpass query to fetch buildings in the specified bounding box
    overpass_query = f"""
    [out:json];
    (
      way["building"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      relation["building"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out body;
    >;
    out skel qt;
    """

    # Send the request to Overpass API
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example bounding box: (southwest_latitude, southwest_longitude, northeast_latitude, northeast_longitude)
bbox = (40.7122, -74.0060, 40.7132, -74.0040)  # New York City (change as needed)

# Fetch building data
buildings_data = fetch_buildings_in_bounding_box(bbox)

# Print building data
if buildings_data:
    for element in buildings_data['elements']:
        building_id = element['id']
        building_type = element['type']
        height = element['tags'].get('height', 'unknown')
        levels = element['tags'].get('building:levels', 'unknown')
        print(f"Building ID: {building_id}, Type: {building_type}, Height: {height}, Levels: {levels}")
