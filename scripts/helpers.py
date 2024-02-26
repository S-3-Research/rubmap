import requests
import time
import json
import tqdm
from urllib.parse import quote
from credentials import GOOGLE_GEOCODING_API_KEY

def get_geocode(cache: dict[str, list], query: str):
    """
    Get the geocode for a given query from the cache or by making an API request.
    args:
        cache: dict, the cache to store the geocoding results
        query: str, the query to geocode
    """
    if query not in cache or cache[query] == "failed":
        result = geocode_address(query)
        if result is not None:
            cache[query] = result
            print(query, "succeeded")
        else:
            cache[query] = "failed"
            print(query, "failed")

def geocode_address(address: str) -> list:
    """
    Geocode the given address using the Google Maps Geocoding API.
    args:
        address: str, the address to geocode
    returns:
        list, the geocoding results from the API
    """
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={quote(address)}&key={GOOGLE_GEOCODING_API_KEY}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                return data['results']
            else:
                print('Address geocoding failed:', data['status'])
        else:
            print('Error occurred while making the API request.')
    except requests.exceptions.RequestException as e:
        print('Error occurred:', e)
    return None

def test_geocode_address():
    """
    Test the geocode_address function.
    """
    print('='*50)
    print('Testing geocode_address function...')
    print('='*50)

    # Example list of addresses
    addresses = ['1600 Amphitheatre Parkway, Mountain View, CA 94043',
                '1 Infinite Loop, Cupertino, CA 95014',
                '350 5th Ave, New York, NY 10118']

    # Dictionary to store geocoding results
    geocoded_data = {}

    # Geocode each address and save the results to the dictionary
    for address in addresses:
        result = geocode_address(address)
        if result is not None:
            geocoded_data[address] = result

    # Print the geocoded data
    for address, result in geocoded_data.items():
        print(address)
        print(result)

    print('='*50)
    print('Testing complete.')
    print('='*50)

def load_json_lines(filename: str) -> list:
    """
    Load a JSON Lines file and return the data as a list of dictionaries.
    args:
        filename: str, the name of the file to load
    returns:
        list, the data loaded from the file
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    return data