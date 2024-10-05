import requests
import time

# Define the URL of your FastAPI endpoint
url = "http://host.docker.internal:3000/api/py/agents" 

while True:
    # Send a GET request to the FastAPI endpoint
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the JSON response
        agents_data = response.json()
        print("Agents data:", agents_data)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    time.sleep(.1)



