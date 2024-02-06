import sqlite3


def create_login_database():
    try:
        conn = sqlite3.connect('login_database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE login_data(
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
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

def actions_login_database(action: str, fields=None, seek_id = None):
    error_msg = "'fields' parameter must be provided."
    if action == 'ADD':
        pass_to_database = "INSERT INTO login_data (user_id, username, password, profile_name, phone_number) VALUES (?, ?, ?, ?, ?)"
    elif action == 'REMOVE':
        if fields is None:
            raise ValueError(f"For 'REMOVE' action, {error_msg}")
        conditions = ' AND '.join(f'{field} = ?' for field in fields)
        pass_to_database = f"DELETE FROM login_data WHERE {conditions}"
    elif action == 'EDIT':
        if fields is None:
            raise ValueError(f"For 'EDIT' action, {error_msg}")
        updates = ', '.join(f'{field} = ?' for field in fields)
        pass_to_database = f"UPDATE login_data SET {updates} WHERE username = ?"
    elif action == 'RETRIEVE':
        pass_to_database = "SELECT profile_name, phone_number, password FROM login_data WHERE username = ?"
    elif action == 'RETRIEVE_2':
        if fields is None:
            raise ValueError(f"For 'RETRIEVE_2' action, {error_msg}")
        if seek_id is not None:
            columns = ', '.join(fields)
            pass_to_database = f"SELECT {columns} FROM login_data WHERE {seek_id} = ?"
        else:
            columns = ', '.join(fields)
            pass_to_database = f"SELECT {columns} FROM login_data WHERE phone_number = ?"
    elif action == 'EXISTS':
        pass_to_database = "SELECT profile_name FROM login_data WHERE phone_number = ?"
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
            profile_name, phone_number, password = data
            print(f"Profile Name: {profile_name}, Phone Number: {phone_number}")
    except sqlite3.Error as e:
        display_error(e)
    return data

def change_username(phone_number, new_username):
    try:
        conn = sqlite3.connect('login_database.db')
        c = conn.cursor()
        query = actions_login_database('RETRIEVE_2', fields=['username', 'password', 'profile_name'], seek_id='phone_number')
        c.execute(query, (phone_number,))
        data = c.fetchone()
        if data is not None:
            old_username, password, profile_name = data
            query = actions_login_database('EDIT', fields=['username'], seek_id='phone_number')
            c.execute(query, (new_username, password, profile_name, phone_number))
            conn.commit()
            print(f"Username changed successfully from {old_username} to {new_username}.")
    except sqlite3.Error as e:
        display_error(e)
    finally:
        if conn:
            conn.close()



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
