import json
import time
import re
import requests
from datetime import datetime

with open('prefs') as f:
    p = json.load(f)

MAPS_KEY = p['google']['maps_key']
PLACES_KEY = p['google']['places_key']


def pull_json_info(lat, lon):
    base = "https://maps.googleapis.com/maps/api/geotweetscode/json?"
    params = "latlng={lat},{lon}&key={key}".format(
        lat=lat, lon=lon, key=MAPS_KEY)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    return response.json()


def pull_formatted_addr(lat, lon):
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&key={key}".format(
        lat=lat, lon=lon, key=MAPS_KEY)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    return response.json()['results'][0]['formatted_address']


def pull_places_nearby(lat, lon):
    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    params = """location={lat},{lon}&radius={rad}&types={types}&key={key}
             """.format(lat=lat, lon=lon, rad=50, types='restaurant',
                        key=PLACES_KEY)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    # most likely will want to store all json & place-id for reference.
    return response.json()


def pull_place_info(place_id):
    base = "https://maps.googleapis.com/maps/api/place/details/json?"
    params = "placeid={place_id}&key={key}".format(
        place_id=place_id, key=PLACES_KEY)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    return response.json()


def time_restate(date_str):
    time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")
    return datetime.fromtimestamp(time.mktime(time_struct))


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''


def extract_re(regex, data_src):
    data_out = []
    for elem in data_src:
        match = re.search(regex, str(elem))
        if match:
            point = str(match.group())
            point = point.split(',')
            point = (point[0][1:].strip(), point[1][:-1].strip())
            data_out.append(point)
    return data_out
