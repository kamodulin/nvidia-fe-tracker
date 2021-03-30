import datetime
import os

def notify(number, item, message, url):
    os.system(f"""osascript -e 'display notification "{message}" with title "{item["name"]}"sound name "Glass"'""")
    os.system(f"""osascript sendMessage.scpt {number} "{item["name"] + " " + message + " " + url}" """)


def pprint(item, text, color):
    status = {
    "OK": "\033[92m",
    "WARN": "\033[93m",
    "FAIL": "\033[91m",
    "END": "\033[0m"
    }

    time = datetime.datetime.now().strftime("%I:%M%p")
    
    start = status[color]
    end = status["END"]

    print(f"{start}[{time} {color}] {text}: {item['name']}{end}")