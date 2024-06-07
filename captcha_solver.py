import requests
import time

def solve_captcha(site_key, site_url, api_key):
    captcha_request_url = 'http://2captcha.com/in.php'
    captcha_request_payload = {
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': site_key,
        'pageurl': site_url,
        'json': 1
    }

    response = requests.post(captcha_request_url, data=captcha_request_payload)
    request_result = response.json()

    if request_result['status'] == 1:
        request_id = request_result['request']
    else:
        print(f"Failed to send CAPTCHA request. Error: {request_result['request']}")
        return None

    captcha_result_url = 'http://2captcha.com/res.php'
    captcha_result_payload = {
        'key': api_key,
        'action': 'get',
        'id': request_id,
        'json': 1
    }

    while True:
        response = requests.get(captcha_result_url, params=captcha_result_payload)
        result = response.json()
        if result['status'] == 1:
            return result['request']
        elif result['request'] == 'CAPCHA_NOT_READY':
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            print(f"Failed to get CAPTCHA solution. Error: {result['request']}")
            return None