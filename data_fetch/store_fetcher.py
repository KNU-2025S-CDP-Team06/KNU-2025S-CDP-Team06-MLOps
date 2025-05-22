import json
import os
import sys
STORE_JSON_PATH = os.path.join(os.path.dirname(__file__), "../stores.json")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from config import config
from . import geocode_converter
import bcrypt

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def load_store_data():
    with open(STORE_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def fetch_store(mb_id:str, name:str):

    url = config.MOKI_STORE_INFO_URL
    params = {
        "mb_id" : mb_id,
        "mb_password" : config.STORE_PASSWORD
    }
    store_data = requests.get(url, params=params).json()
    
    address = store_data["mb_addr"]
    if address == " ":
        address = config.TEMPORARY_ADDRESS
    
    latitude, longitude = geocode_converter.convert(address)
    store_info = {
        "mb_id" : mb_id,
        "password" : hash_password(config.STORE_PASSWORD),
        "name" : name,
        "address" : address,
        "latitude" : latitude,
        "longitude" : longitude,
        "Role" : "STORE"
    }

    return store_info