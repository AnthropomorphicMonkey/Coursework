import hashlib
# http://bobby-tables.com/python guidance followed to avoid SQL injection
import sqlite3
import uuid

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


def check_user_exists(username):
    # Finds the number of occurrences in the users table of the inputted username. If 0 returned, username is not in DB
    sql = "SELECT COUNT(1) FROM users WHERE username = ?;"
    c.execute(sql, (username,))
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


# Assumes valid username provided
def find_salt(username):
    # Finds the salt for the given username
    sql = "SELECT password_salt FROM users WHERE username = ?;"
    c.execute(sql, (username,))
    salt = c.fetchall()[0][0]
    # Takes the SQL output and formats appropriately to give just a string
    return salt


# Assumes valid username and salt provided
def check_hash(username, password, salt):
    generated_hash = generate_hash(password, salt)
    # Verifies username and hash are in database by counting number of times they occur together
    # This will be either 0 or 1 (not present, present)
    sql = 'SELECT COUNT(1) FROM users WHERE username = ? AND password_hash = ?;'
    c.execute(sql, (username, generated_hash))
    # If generated hash matched stored hash for given username return true, otherwise return false
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


def generate_hash(password, salt):
    # Combines password and salt and generates SHA256 hash of combined phrase
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


# Assumes valid username
def check_password(username, password):
    return check_hash(username, password, find_salt(username))


def generate_salt():
    return uuid.uuid4().hex


def create_account(username, password, first_name, last_name, account_type):
    # Generates a unique random salt
    salt = generate_salt()
    sql = "INSERT INTO users(username, password_salt, password_hash, first_name, last_name, account_type) " \
          "VALUES(?, ?, ?, ?, ?, ?);"
    # Executes SQL to insert a correctly formatted record into the users table
    c.execute(sql,
              (username.casefold(), salt, generate_hash(password, salt), first_name.casefold(), last_name.casefold(),
               account_type))
    conn.commit()


if __name__ == '__main__':
    # Area to be used for testing purposes use username test, password test12345
    un = input("Enter username: ")
    pw = input("Enter password: ")
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    user_type = input("Enter user type ('s' or 't'): ")
    create_account(un, pw, first, last, user_type)
