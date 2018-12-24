import sqlite3

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


def get_classes_of_user(user_id):
    sql = 'SELECT classes.id, classes.name ' \
          'FROM ((class_user INNER JOIN classes ON class_user.class_id = classes.id)INNER JOIN users ON users.id) ' \
          'WHERE users.id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()
