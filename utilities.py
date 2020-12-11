import datetime
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def notify(title, text, sound, url, imessage_number):
    os.system("""osascript -e 'display notification "{}" with title "{}"sound name "{}"'""".format(text, title, sound))
    os.system("""osascript sendMessage.scpt "{}" "{}" """.format(imessage_number,'CARD: ' + title + '\n STATUS: ' + text + ' ' + url)) 

def printer(status_code, gpu, text, color, sleep=False):
    now = datetime.datetime.now().strftime("%I:%M%p")
    if sleep:
        string = f'{color}[{now} {status_code}] {text}{bcolors.ENDC}'
    else:
        string = f'{color}[{now} {status_code}] {bcolors.BOLD}{gpu}{bcolors.ENDC}{color}: {text}{bcolors.ENDC}'
    print(string)