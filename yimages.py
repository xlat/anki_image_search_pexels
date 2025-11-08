import re
import json
import requests
import urllib.parse

from . import utils

requests.packages.urllib3.disable_warnings()

BASE_URL = 'https://api.pexels.com/v1/search?query='
headers = {
    "Authorization": utils.get_api_key(),
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

def make_pexels_url(query):
    return BASE_URL + urllib.parse.quote_plus(query) + '&size=small&per_page=15'  # Adjust per_page as needed (max 80)

def get_pexels_response(query):
    url = make_pexels_url(query)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Raise error for bad status codes
        return r.json()
    except requests.exceptions.RequestException as e:
        utils.report('Request error\n\n' + str(e) + '\n\nURL: ' + url)
        return None
    except json.JSONDecodeError as e:
        utils.report('JSON decode error\n\n' + str(e) + '\n\nResponse: ' + r.text[:200])
        return None


def parse_pexels_response(response):
    result = []

    try:
        if 'photos' not in response:
            utils.report('No photos found in response\n\n' + str(response))
            return result

        for photo in response['photos']:
            # Use 'medium' size for flashcards; options: tiny, small, medium, large, original
            image_url = photo['src']['medium']
            result.append(image_url)
    except Exception as e:
        utils.report('Error parsing JSON response\n\n' + repr(e))
        return result

    return result


def get_yimages(query):
    # Note: Function name kept for compatibility, but now uses Pexels
    response = get_pexels_response(query)
    return parse_pexels_response(response)