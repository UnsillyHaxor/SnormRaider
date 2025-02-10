import json
import requests
import os
from concurrent.futures import ThreadPoolExecutor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(title):
    print(f"{'=' * 60}\n{title}\n{'=' * 60}")

def print_error(message):
    print(f"Error: {message}")

def print_info(message):
    print(f"{message}")

def send_dm_to_user(token_discord, user_id, message, count):
    try:
        response = requests.post("https://discord.com/api/v9/users/@me/channels",
                                 headers={'Authorization': token_discord, 'Content-Type': 'application/json'},
                                 json={"recipient_id": user_id})
        if response.status_code == 200:
            channel_id = response.json()['id']
            for i in range(count):
                send_message_response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages",
                                                      headers={'Authorization': token_discord, 'Content-Type': 'application/json'},
                                                      json={"content": message})
                if send_message_response.status_code == 200:
                    print_info(f"Message {i+1}/{count} sent to user ID: {user_id} using token {token_discord[:10]}...")
                else:
                    print_error(f"Failed to send message {i+1}/{count}. Status code {send_message_response.status_code}: {send_message_response.text}")
        else:
            print_error(f"Failed to create DM channel. Status code {response.status_code}: {response.text}")
    except Exception as e:
        print_error(f"Error sending DM: {e}")

def send_dm_to_user_multiple_tokens(token_list, user_id, message, count):
    def send_messages_with_token(token):
        send_dm_to_user(token, user_id, message, count)

    try:
        with ThreadPoolExecutor() as executor:
            executor.map(send_messages_with_token, token_list)

        input("All DMs sent! Press Enter to return to the main menu...")

    except Exception as e:
        print_error(f"Error: {e}")

def send_message_to_channel(token_discord, channel_id, message, count):
    for i in range(count):
        try:
            response = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers={'Authorization': token_discord, 'Content-Type': 'application/json'},
                json={"content": message}
            )
            if response.status_code == 200:
                print_info(f"Message {i+1}/{count} sent successfully with token {token_discord[:10]}...")
            else:
                print_error(f"Failed with token {token_discord[:10]} - Status code {response.status_code}: {response.text}")
        except Exception as e:
            print_error(f"Error with token {token_discord[:10]}: {e}")

def execute_single_dm():
    try:
        clear()
        print_title("DM SPAMMER")

        token_discord = input("Enter your Discord token: ").strip()
        user_id = input("Enter the user ID to DM: ").strip()
        message = input("Enter the message to send: ").strip()
        count = int(input("Enter how many times to send the message: ").strip())

        if not token_discord or not user_id or not message or count <= 0:
            print_error("All fields are required, and the count must be greater than 0. Please try again.")
            return

        send_dm_to_user(token_discord, user_id, message, count)

        input("Press Enter to return to the main menu...")

    except Exception as e:
        print_error(f"Error: {e}")

def execute_channel_spammer():
    try:
        clear()
        print_title("CHANNEL SPAMMER WITH MULTIPLE TOKENS")

        file_path = input("Enter the path to the file containing tokens (one per line): ").strip()
        channel_id = input("Enter the channel ID to send messages to: ").strip()
        message = input("Enter the message to send: ").strip()
        count = int(input("Enter how many times each token should send the message: ").strip())

        if not os.path.exists(file_path):
            print_error("The specified file does not exist. Please check the path and try again.")
            return

        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]

        if not tokens:
            print_error("No tokens found in the file. Please check the file and try again.")
            return

        def send_messages_with_token(token):
            send_message_to_channel(token, channel_id, message, count)

        with ThreadPoolExecutor() as executor:
            executor.map(send_messages_with_token, tokens)

        input("All messages sent! Press Enter to return to the main menu...")

    except Exception as e:
        print_error(f"Error: {e}")

def execute_multiple_user_dm():
    try:
        clear()
        print_title("MULTI-TOKEN DM SPAMMER")

        file_path = input("Enter the path to the file containing tokens (one per line): ").strip()
        user_id = input("Enter the user ID to DM: ").strip()
        message = input("Enter the message to send: ").strip()
        count = int(input("Enter how many times each token should send the message: ").strip())

        if not os.path.exists(file_path):
            print_error("The specified file does not exist. Please check the path and try again.")
            return

        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]

        if not tokens:
            print_error("No tokens found in the file. Please check the file and try again.")
            return

        send_dm_to_user_multiple_tokens(tokens, user_id, message, count)

    except Exception as e:
        print_error(f"Error: {e}")

def display_menu():
    clear()

    menu = f"""
1. Raid someones dms ( one token ) Made by Snormware
2. Raid a channel ( multiple tokens ) Made by Snormware 
3. Raid someones dms ( multiple tokens ) https://discord.gg/TKejEpnEAx https://www.youtube.com/@snormware
4. Exit
    """
    print(menu)

def handle_menu_choice(choice):
    if choice == '1':
        execute_single_dm()
    elif choice == '2':
        execute_channel_spammer()
    elif choice == '3':
        execute_multiple_user_dm()
    elif choice == '4':
        print_info("Exiting program. Press Enter to close.")
        input()
        exit(0)
    else:
        print_error("Invalid choice. Please enter a valid option.")

def run_menu():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        handle_menu_choice(choice)

if __name__ == "__main__":
    run_menu()
