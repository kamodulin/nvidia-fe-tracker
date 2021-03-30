import logging
import json
import random
import requests
import time

from bs4 import BeautifulSoup

from utilities import notify, pprint

class Scraper:
    def __init__(self):
        self.load_data()
        self.notifications = 0
        self.active = True        

    def load_data(self):
        with open("data.json") as f:
            data = json.load(f)
        
        for key, values in data.items():
            setattr(self, key, values)
    
    def start(self):
        while self.active:
            self.fetch()
            self.random_pause()

    def fetch(self):
        item = self.random_item()
        headers = self.random_headers()

        try:            
            response = requests.get(item["url"], headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            if item["target"]["type"] == "class":
                label = soup.find_all(class_=item["target"]["name"])[0].get_text()

            elif item["target"]["type"] == "id":
                label = soup.find_all(id=item["target"]["name"])[0].get_text()

            if label == item["keyword"]:
                pprint(item, label, "OK")
                self.alert(item, label)
            
            else:
                pprint(item, label, "WARN")
            
        except Exception as e:
            pprint(item, e, "FAIL")
            self.alert(item, e)

    def stop(self):
        self.active = False
        logging.info("Scraper stopped")

    def random_pause(self):
        pause = random.uniform(0, self.options["pause"])
        long_pause = random.uniform(0, self.options["long_pause"])
        
        p = random.random()

        if p <= self.options["long_pause_proba"]:
            print(f"Sleeping for {round(long_pause, 1)}s")
            time.sleep(long_pause)
        
        else:
            time.sleep(pause)

    def random_item(self):
        return random.choice(self.products)
    
    def random_headers(self):
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
            }

        return headers

    def alert(self, item, message):
        try:
            for number in self.imessage_numbers:
                notify(number, item, message)
        except:
            pass
        
        self.notifications += 1
        
        if self.notifications >= self.options["max_notifications"]:
            self.stop()        

if __name__ == "__main__":
    scrape = Scraper()
    scrape.start()