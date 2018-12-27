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


def get_homework_score(user_id, homework_id):
    sql = 'SELECT question_results.attempts, question_results.correct ' \
          'FROM ((homework INNER JOIN homework_questions ON homework.id = homework_questions.homework_id)' \
          'INNER JOIN questions ON homework_questions.question_id = questions.id) ' \
          'INNER JOIN question_results ON questions.id = question_results.question_id ' \
          'WHERE question_results.user_id = ? AND homework.id = ?'
    c.execute(sql, (user_id, homework_id))
    scores = c.fetchall()
    sql = 'SELECT homework.name, class_homework.due_date ' \
          'FROM homework INNER JOIN class_homework on homework.id = class_homework.homework_id ' \
          'WHERE homework.id = ?'
    c.execute(sql, (homework_id,))
    name_due_date = c.fetchall()[0]
    return name_due_date[0], scores, name_due_date[1]


if __name__ == '__main__':
    print(get_homework_score(1, 1))
