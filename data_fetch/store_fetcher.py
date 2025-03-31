import json
import os
import sys
STORE_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/stores.json")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from config import config
import geocode_converter

def load_store_data():
    with open(STORE_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def fetch_store(mb_id:str, name:str):
    url = config.MOKI_STORE_INFO_URL+f"mb_id={mb_id}"+f"&mb_password={config.STORE_PASSWORD}"
    store_data = requests.get(url).json()
    address = store_data["mb_addr"]
    if address == " ":
        address = config.TEMPORARY_ADDRESS
    
    latitude, longitude = geocode_converter.convert(address)
    store_info = {
        "mb_id" : mb_id,
        "name" : name,
        "address" : address,
        "latitude" : latitude,
        "longitude" : longitude
    }

    return store_info