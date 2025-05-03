import sys
import os
import requests
from datetime import datetime
from pprint import pprint
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

def load_menu(mb_id: str):
    params = {
        "mb_id" : mb_id
    }
    url = config.MOKI_MENU_API_URL
    menu_info = requests.get(url, params=params).json()['data']

    return menu_info