import time
import random
import string
import json
import requests
import logging

def generate_unique_email():
    timestamp = int(time.time())
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{timestamp}{random_str}@bajerergodt.com"

def send_request(method, url, **kwargs):
    try:
        response = method(url, **kwargs)
        response.raise_for_status()
        return response.json(), response.cookies.get_dict()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None, None

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
