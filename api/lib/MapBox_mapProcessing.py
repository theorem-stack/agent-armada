import requests
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# This code snippet fetches a terrain tile from Mapbox and converts it to an elevation map.
# https://docs.mapbox.com/data/tilesets/guides/access-elevation-data/

def lat_lon_to_tile(lat, lon, zoom):
    """Convert latitude and longitude to tile coordinates."""
    n = 2 ** zoom
    x = int(n * (lon + 180) / 360)
    y = int(n * (1 - (np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)) / np.pi)))
    return x, y

def fetch_tile(z, x, y, access_token):
    """Fetch a terrain tile from Mapbox."""
    url = f'https://api.mapbox.com/styles/v1/mapbox/terrain-rgb/tiles/{z}/{x}/{y}?access_token={access_token}'
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def calculate_elevation(image, detail):
    """Calculate elevation from RGB values."""
    rgb_array = np.array(image)
    height, width, _ = rgb_array.shape
    elevation_array = np.zeros((height // detail, width // detail))

    for i in range(0, height, detail):
        for j in range(0, width, detail):
            R, G, B = rgb_array[i, j]
            elevation = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
            elevation_array[i // detail, j // detail] = elevation
            
    return elevation_array

# Replace with your own values
access_token = 'YOUR_ACCESS_TOKEN'
zoom = 12  # Zoom level
latitude = 34.0522  # Latitude of the desired location
longitude = -118.2437  # Longitude of the desired location
detail = 2  # Step size for height map (1 = full resolution, 2 = half, etc.)

# Convert lat/lon to tile coordinates
x, y = lat_lon_to_tile(latitude, longitude, zoom)

# Fetch and process the tile
tile_image = fetch_tile(zoom, x, y, access_token)
elevation_map = calculate_elevation(tile_image, detail)

# Visualize the elevation map
plt.imshow(elevation_map, cmap='terrain')
plt.colorbar(label='Elevation (meters)')
plt.title('Elevation Map from Latitude/Longitude')
plt.show()
