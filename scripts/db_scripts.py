import hashlib
# http://bobby-tables.com/python guidance followed to avoid SQL injection
import sqlite3
import uuid

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


def check_user_exists(username: str) -> bool:
    # Finds the number of occurrences in the users table of the inputted username. If 0 returned, username is not in DB
    sql: str = 'SELECT COUNT(1) FROM users WHERE username = ?;'
    c.execute(sql, (username,))
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


# Assumes valid username provided
def find_salt(user_id: int) -> str:
    # Finds the salt for the given username
    sql: str = 'SELECT password_salt FROM users WHERE id = ?;'
    c.execute(sql, (user_id,))
    salt: str = c.fetchall()[0][0]
    # Takes the SQL output and formats appropriately to give just a string
    return salt


# Assumes valid user id and salt provided
def check_hash(user_id: int, password: str, salt: str) -> bool:
    generated_hash: str = generate_hash(password, salt)
    # Verifies user id and hash are in database by counting number of times they occur together
    # This will be either 0 or 1 (not present, present)
    sql: str = 'SELECT COUNT(1) FROM users WHERE id = ? AND password_hash = ?;'
    c.execute(sql, (user_id, generated_hash))
    # If generated hash matched stored hash for given username return true, otherwise return false
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


def generate_hash(password: str, salt: str) -> str:
    # Combines password and salt and generates SHA256 hash of combined phrase
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


# Assumes valid username
def check_password(user_id: int, password: str) -> bool:
    # Returns whether password entered for given user id is valid
    return check_hash(user_id, password, find_salt(user_id))


def generate_salt() -> str:
    # Securely generates a random salt
    return uuid.uuid4().hex


def create_account(username: str, password: str, first_name: str, last_name: str, account_type: str):
    # Generates a unique random salt
    salt: str = generate_salt()
    sql: str = 'INSERT INTO users(username, password_salt, password_hash, first_name, last_name, type)' \
               'VALUES(?, ?, ?, ?, ?, ?);'
    # Executes SQL to insert a correctly formatted record into the users table
    c.execute(sql,
              (username.casefold(), salt, generate_hash(password, salt), format_name(first_name),
               format_name(last_name), account_type))
    conn.commit()


def get_user_id(username: str) -> int:
    # Returns user id from database for given username
    sql: str = 'SELECT id FROM users WHERE username = ?;'
    c.execute(sql, (username,))
    return c.fetchall()[0][0]


def get_account_type(user_id: int) -> str:
    # Returns account type from database for given id
    sql: str = 'SELECT type FROM users WHERE id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()[0][0]


def get_username(user_id: int) -> str:
    # Returns username from database for given id
    sql: str = 'SELECT username FROM users WHERE id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()[0][0]


def get_first_name(user_id: int) -> str:
    # Returns first name from database for given id
    sql: str = 'SELECT first_name FROM users WHERE id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()[0][0]


def get_last_name(user_id: int) -> str:
    # Returns last name from database for given id
    sql: str = 'SELECT last_name FROM users WHERE id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()[0][0]


def update_first_name(user_id: int, new_first_name: str):
    # Updates value for first name in database for given id
    sql: str = 'UPDATE users SET first_name = ? WHERE id = ?;'
    c.execute(sql, (format_name(new_first_name), user_id))
    conn.commit()


def update_last_name(user_id: int, new_last_name: str):
    # Updates value for last name in database for given id
    sql: str = 'UPDATE users SET last_name = ? WHERE id = ?;'
    c.execute(sql, (format_name(new_last_name), user_id))
    conn.commit()


def format_name(first_name: str) -> str:
    # Formats a first or last name for the database (all lowercase)
    return first_name.casefold()


def update_password(user_id: int, password: str):
    # Updates value for hashed password in database for given id
    sql: str = 'UPDATE users SET password_hash = ? WHERE id = ?;'
    c.execute(sql, (generate_hash(password, find_salt(user_id)), user_id))
    conn.commit()


if __name__ == '__main__':
    # Area to be used for testing purposes use username test, password test12345
    print(get_first_name(1))
    un: str = input("Enter username: ")
    pw: str = input("Enter password: ")
    first: str = input("Enter first name: ")
    last: str = input("Enter last name: ")
    user_type: str = input("Enter user type ('s' or 't'): ")
    create_account(un, pw, first, last, user_type)
