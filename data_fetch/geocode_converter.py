import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from config import config

def convert(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    header = {'Authorization': 'KakaoAK ' + config.KAKAO_REST_API_KEY}

    r = requests.get(url, headers=header)
    if r.status_code == 200:
        lng = float(r.json()["documents"][0]["address"]['x'])
        lat = float(r.json()["documents"][0]["address"]['y'])
    else:
        return 0, 0
    
    return lat, lng