import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import subprocess 
import logging
from colorama import init, Fore, Style
import colorama

colorama.init()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
logo = r"""
             ██████╗ ███████╗ ██████╗██████╗ 
             ██╔══██╗██╔════╝██╔════╝██╔══██╗
             ██████╔╝█████╗  ██║     ██████╔╝
             ██╔══██╗██╔══╝  ██║     ██╔═══╝ 
             ██║  ██║██║     ╚██████╗██║     
             ╚═╝  ╚═╝╚═╝      ╚═════╝╚═╝  [V1]
             ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ ʟᴇɪɴᴀᴛʜᴀɴ ᴏʀᴇᴍᴏʀ
"""

def display_logo():
    logo = """
    \033[1;34m██████╗ ███████╗ ██████╗██████╗ 
              ██╔══██╗██╔════╝██╔════╝██╔══██╗
              ██████╔╝█████╗  ██║     ██████╔╝
              ██╔══██╗██╔══╝  ██║     ██╔═══╝ 
              ██║  ██║██║     ╚██████╗██║     
              ╚═╝  ╚═╝╚═╝      ╚═════╝╚═╝  [V1]\033[0m
              \033[1;32mRFCP TOOLS\033[0m
    """
    print(logo)
def get_approval_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def approval():
    clear_console()
    print(Fore.CYAN + logo + Style.RESET_ALL)  # Display logo in cyan
    user_id = str(os.geteuid())
    uuid = f"{user_id}DS{user_id}"
    key = f"RFCP-{uuid}"

    print("\033[1;37m [\u001b[36m•\033[1;37m] You Need Approval To Use This Tool   \033[1;37m")
    print(f"\033[1;37m [\u001b[36m•\033[1;37m] Your Key :\u001b[36m {key}")
    
    urls = [
        "https://github.com/rfcptoolsofficial/approval/blob/main/approval.txt"
    ]
    
    key_found = False
    for url in urls:
        approval_data = get_approval_data(url)
        if key in approval_data:
            key_found = True
            break

    if key_found:
        print(f"\033[1;97m >> Your Key Has Been Approved!!!")
        return key
    else:
        
        exit()

def countdown(delay):
    icons = ['X    ', ' X   ', '  X  ', '   X ', '    X']
    while delay > 0:
        for i in range(5):
            print(f"\033[1;37m[DELAY][{icons[i]}][{delay} seconds]", end='\r')
            sleep(0.2)
        delay -= 1

class Machine:
    def __init__(self):
        self.session_list = []
        self.delay = 0
        self.url = None
        self.reactions_dict = {
            '1': 'like', 
            '2': 'love', 
            '3': 'care', 
            '4': 'haha', 
            '5': 'wow', 
            '6': 'sad', 
            '7': 'angry'
        }
        self.selected_reactions = []
        self.logged_in_accounts = []
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.5',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A037F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        }

    def boost_reaction(self, session):
        try:
            get_token = session.get('https://machineliker.net/auto-reactions').text
            token = re.search(r'name="_token" value="(.*?)"', get_token).group(1)
            hash_ = re.search(r'name="hash" value="(.*?)"', get_token).group(1)

            data = {
                'url': self.url,
                'limit': '25',
                'reactions[]': self.selected_reactions,
                '_token': token,
                'hash': hash_
            }

            response = session.post('https://machineliker.net/auto-reactions', headers=self.headers, data=data).text
            
            if "Error!" in response and "please try again after" in response:
                minutes = int(re.search(r'please try again after (\d+) minutes', response).group(1))
                self.delay = minutes * 60
                print(f"\033[1;91mCooldown: Please wait {self.delay} seconds more\033[0m")
            elif 'Order Submitted' in response:
                print(f"\033[1;92mSuccessfully increased reactions from {session}\033[0m")
                self.delay = 10
            else:
                print("\033[1;91mUnexpected error occurred\033[0m")
        except Exception as e:
            print(f"\033[1;91mError boosting reaction: {e}\033[0m")

    def login(self, fb_cookie):
        try:
            session = requests.Session()
            session.get('https://machineliker.net/login')
            headers = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A037F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
                'x-xsrf-token': session.cookies.get('XSRF-TOKEN').replace('%3D', '=')
            }
            data = {'session': fb_cookie}
            response = session.post('https://machineliker.net/login', headers=headers, data=data).json()
            
            if response['success']:
                name = response['user']['name']
                user_id = response['user']['id']
                self.logged_in_accounts.append(f"{user_id} | {name}")
                return session
            else:
                print(f"\033[1;91mLogin Failed! Invalid Facebook Cookie: {fb_cookie.split('c_user=')[1].split(';')[0]}\033[0m")
                return None
        except Exception as e:
            print(f"\033[1;91mLogin error: {e}\033[0m")
            return None

    def get_cookies(self):
        while True:
            try:
                cookie_count = int(input("\033[1;33mHow many cookies do you want to enter? (1-5): \033[0m"))
                if 1 <= cookie_count <= 5:
                    break
                print("\033[1;91mPlease enter a valid number between 1 and 5.\033[0m")
            except ValueError:
                print("\033[1;91mInvalid input. Please enter a number.\033[0m")

        self.cookies = {}
        
        for i in range(cookie_count):
            while True:
                fb_cookie = input(f"\033[1;33mEnter Facebook cookie for account {i + 1}: \033[0m").strip()
                if fb_cookie:
                    self.cookies[f"cookie{i + 1}"] = fb_cookie
                    break
                print("\033[1;91mYou must enter a valid cookie.\033[0m")

    def main(self):
        
        clear_console()
        approval()
      
        while True:
            self.get_cookies()

            with ThreadPoolExecutor() as executor:
                for fb_cookie in self.cookies.values():
                    session = executor.submit(self.login, fb_cookie).result()
                    if session:
                        self.session_list.append(session)

            if self.session_list:
                break
            else:
                print("\033[1;91mNo valid sessions logged in. Please re-enter cookies.\033[0m")
                self.session_list.clear()

        clear_console()
        
       
        print("\nLogged in accounts:")
        for account in self.logged_in_accounts:
            print(f"\033[1;32m- {account}\033[0m")

        self.url = input("\033[1;34mEnter the URL of the post to boost reactions: \033[0m")
        print("\033[1;32mChoose the reaction type(s) to boost (e.g., 123 for like, love, and care):\033[0m")
        print("\033[1;32m1: like\n2: love\n3: care\n4: haha\n5: wow\n6: sad\n7: angry\033[0m")
        choices = input("Enter the numbers: ")
        self.selected_reactions = [self.reactions_dict[x] for x in choices]

        while True:
            for session in self.session_list:
                self.boost_reaction(session)
            countdown(self.delay)

if __name__ == '__main__':
    clear_console()
    display_logo()
    Machine().main()
