import sqlite3


def create_login_database():
    try:
        conn = sqlite3.connect('login_database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE login_data(
                username INTEGER PRIMARY KEY,
                password TEXT NOT NULL,
                profile_name TEXT NOT NULL,
                phone_number INTEGER NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        display_error(e)
    finally:
        conn.close()

def display_error(e):
    error_message = ' '.join(e.args)
    print(f'ERROR: {error_message}')

def actions_login_database(action: str):
    if action == 'ADD':
        pass_to_database = "INSERT INTO login_data (username, password, profile_name, phone_number) VALUES (?, ?, ?, ?)"
    elif action == 'REMOVE':
        pass_to_database = "DELETE FROM login_data WHERE username = ?"
    elif action == 'EDIT':
        pass_to_database = "UPDATE login_data SET password = ?, profile_name = ?, phone_number = ? WHERE username = ?"
    elif action == 'RETRIEVE':
        pass_to_database = "SELECT profile_name, phone_number FROM login_data WHERE username = ?"
    return pass_to_database

def retrieve_data(username):
    try:
        conn = sqlite3.connect('login_database.db')
        c = conn.cursor()
        query = actions_login_database('RETRIEVE')
        c.execute(query, (username,))
        data = c.fetchone()
        conn.close()
        if data is None:
            print("No data found for this username.")
        else:
            profile_name, phone_number = data
            print(f"Profile Name: {profile_name}, Phone Number: {phone_number}")
    except sqlite3.Error as e:
        display_error(e)
    return data

def add_to_database(profile: tuple):
    try:
        conn = sqlite3.connect('login_database.db')
        c = conn.cursor()
        query = actions_login_database('ADD')
        c.execute(query, profile)
        conn.commit()
        print(f"User {profile[0]} added successfully.")
    except sqlite3.Error as e:
        display_error(e)
    finally:
        if conn:
            conn.close()
