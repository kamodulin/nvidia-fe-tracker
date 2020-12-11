import time
import datetime
import os

import requests
import numpy as np
from bs4 import BeautifulSoup

from inventory import user_agents, gpus
from utilities import *

IMESSAGE_PHONE_NUMBER = 8001234567 #REPLACE with own iMessage-enabled phone number
BUFFER = 5
DELAY_MAX = 2 #DEFAULT=2
LONG_PAUSE_MAX = 15 #DEFAULT=15
LONG_PAUSE_THRESH = 0.07 #DEFAULT=0.07
MAX_NOTIFICATIONS = 4

buffer = BUFFER
notification_counter = 0

while True:        
    if notification_counter >= MAX_NOTIFICATIONS:
        print('Too many notifications. Reset required.')
        break

    random_pause = np.random.random_sample()

    if random_pause < LONG_PAUSE_THRESH and buffer <= 0:
        pause = np.random.random_sample() * LONG_PAUSE_MAX 
        printer('SLEEP', '', f'Paused fetching for {pause:.2f}s.', bcolors.HEADER, sleep=True)
        time.sleep(pause)
        
        buffer = BUFFER
        pass

    user_agent = np.random.choice(user_agents)

    gpu = np.random.choice(gpus)

    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'www.bestbuy.com',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
        }

    delay = np.random.random_sample() * DELAY_MAX

    try:
        start = time.time()
        response = requests.get(gpu['url'], headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            button_label = soup.find_all(class_='fulfillment-add-to-cart-button')[0].get_text()

        except Exception as e:
            button_label = 'LABEL NOT FOUND'

        fetch_time = time.time() - start

        if button_label != gpu['keyword']:
            notify(f"{gpu['name']} - Retrieved {fetch_time:.2f}s ago", f"{button_label}", "Glass", gpu['url'], IMESSAGE_PHONE_NUMBER)
            printer(response.status_code, gpu['name'], f'{button_label}', bcolors.OKGREEN)
            notification_counter += 1
            
        else:    
            printer(response.status_code, gpu['name'], f"{button_label}. Retrieved: {fetch_time:.2f}s ago. Pause p: {random_pause:.2f}. Delay: {delay:.2f}s.", bcolors.FAIL)
        
    except Exception as e:
        notify(f"{gpu['name']}", f"{e}", "Glass", gpu['url'], IMESSAGE_PHONE_NUMBER)
        printer(e, gpu['name'], f"Failed to get response.", bcolors.WARNING)
        notification_counter += 1
        pass

    time.sleep(delay)
    buffer -= 1