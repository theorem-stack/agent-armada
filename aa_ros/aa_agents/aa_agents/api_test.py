import requests
import time

# url = "http://localhost:8000/api/py/agents"  # for local use
url = f"http://host.docker.internal:8000/api/py/agents" # for use in docker

while True:
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()

        if response.status_code == 200:
            agents_data = response.json()
            print("Agents data:", agents_data)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        exit(1)

    time.sleep(1/10)



