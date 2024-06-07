import time
import random
import requests
import logging
import csv
from config import API_KEY, SITE_URL, SITE_KEY, LOG_FILE, WINNERS_FILE
from captcha_solver import solve_captcha
from helpers import generate_unique_email, send_request, setup_logging

def get_token(session):
    json_data = {'s_source': None}
    response, cookies = send_request(session.post, 'https://game.scratcher.io/winawhopper/visit', json=json_data)
    if response:
        return response['token'], cookies
    return None, None

def register_user(session, token, cookies, captcha_solution):
    unique_email = generate_unique_email()
    json_data = {
        'token': token,
        'full_name': 'Navn',
        'email': unique_email,
        'g-recaptcha-response': captcha_solution,
        'cb_konkurrencebetingelser': '1',
        'cb_markedsforing': '1',
        '__qp_': {},
        's_source': None,
    }
    response, _ = send_request(session.post, 'https://game.scratcher.io/winawhopper/register', cookies=cookies, json=json_data)
    if response:
        return response.get('login_token'), unique_email
    return None, None

def finish_game(session, token, cookies):
    json_data = {
        'data': {'playing_time': 6086},
        'token': token,
        's_source': None,
    }
    response, _ = send_request(session.post, 'https://game.scratcher.io/winawhopper/finish', cookies=cookies, json=json_data)
    return response

def save_winner(email, prize):
    with open(WINNERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, prize])


def play_game():
    print("Starting a new session...")
    logging.info("Starting a new session...")
    session = requests.Session()
    token, cookies = get_token(session)
    if not token:
        logging.error("Failed to get token.")
        return

    captcha_solution = solve_captcha(SITE_KEY, SITE_URL, API_KEY)
    if not captcha_solution:
        logging.error("Failed to solve CAPTCHA.")
        return

    login_token, email = register_user(session, token, cookies, captcha_solution)
    if not login_token:
        logging.error("Failed to register user.")
        return

    cookies.update({'_auth_sc_c_28828_log_tok': login_token})
    response = finish_game(session, token, cookies)
    if response:
        prize = response.get('prize_name')
        logging.info(f"Game finished successfully for {email} with prize {prize}")
        if response.get('winner'):
            save_winner(email, prize)
            logging.info(f"Email {email} won: {prize}")
            print(f"Email {email} won: {prize}")
        else:
            print(f"Email {email} did not win.")
            logging.info(f"Email {email} did not win.")
    else:
        logging.error("Failed to finish game.")


def main():
    setup_logging(LOG_FILE)
    while True:
        play_game()
        wait_time = random.randint(60, 180)  # 1 to 3 minutes
        print(f"Waiting for {wait_time} seconds before sending request")
        logging.info(f"Waiting for {wait_time} seconds before sending request")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
