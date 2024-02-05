import hashlib
import re
import random
import time
import create_databases

def send_code(phone_number):
    pass

def forgot_username():
    # change username if forgotten
    pass

def forgot_password(user):
    # change passwords if forgotten
    print("A 6-digit code will be sent to your phone number.")
    data = create_databases.retrieve_data(user)
         # should be gotten using the username above
    profile_name,phone_number = data


    code = random.randint(100000, 999999)
    send_code(phone_number)

    start_time = time.time()
    while True:
        if time.time() - start_time > 120:
            print("Time's up! Please try again.")
            return

        entered_code = input("Enter the 6-digit code: ")
        if entered_code == str(code):
            new_password = input("Enter your new password: ")
            # Here you would add the logic to change the password in the database
            print("Your password has been changed successfully.")
            return
        else:
            print("Incorrect code. Please try again.")
    pass

def login():
    # asks the user to login and input password and username
    # if successful, no clue just do something...
    pass

def get_profile_details():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    hashed_password = hash_password(password)
    profile_name = input("Choose a profile name: ").strip()

    phone_number = input("Enter your phone number: ").strip()
    cleaned_phone_number = re.sub(r'\D', '', phone_number)

    return username, hashed_password, profile_name, cleaned_phone_number


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def run():
    while True:
        print("1. Login")
        print("2. Forgot Password")
        print("3. Forgot Username")
        print("4. Create Account")
        print("5. Exit")
        action = input("Choose an action: ").strip()

        if action == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login(username, password)
        elif action == '2':
            username = input("Enter your username: ")
            forgot_password(username)
        elif action == '3':
            forgot_username()
        elif action == '4':
            details = get_profile_details()
            create_databases.add_to_database(details)
        elif action == '5':
            break
        else:
            print("Invalid option. Please try again.")


# class LoginSystemWidget:
#     def __init__(self):
#         pass


