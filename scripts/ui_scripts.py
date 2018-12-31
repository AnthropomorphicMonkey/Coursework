import sqlite3

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


def get_classes_of_user(user_id: int) -> list:
    sql = 'SELECT classes.id, classes.name ' \
          'FROM ((class_user INNER JOIN classes ON class_user.class_id = classes.id)' \
          'INNER JOIN users ON users.id = class_user.student_id) ' \
          'WHERE users.id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()


def get_homework_ids(class_id) -> list:
    sql = 'SELECT homework.id ' \
          'FROM homework INNER JOIN class_homework ON homework.id = class_homework.homework_id ' \
          'WHERE class_homework.class_id = ?;'
    c.execute(sql, (class_id,))
    ids = []
    for each_id in c.fetchall():
        ids.append(each_id[0])
    return ids


def get_homework_score(user_id: int, homework_id: int) -> tuple:
    sql = 'SELECT question_results.attempts, question_results.correct ' \
          'FROM ((homework INNER JOIN homework_questions ON homework.id = homework_questions.homework_id)' \
          'INNER JOIN questions ON homework_questions.question_id = questions.id) ' \
          'INNER JOIN question_results ON questions.id = question_results.question_id ' \
          'WHERE question_results.user_id = ? AND homework.id = ?'
    c.execute(sql, (user_id, homework_id))
    score_list = c.fetchall()
    question_count = 0
    score = 0
    for each_score in score_list:
        question_count += 1
        if each_score[1] == 'T':
            score += (1 / each_score[0])
    try:
        result = round(score / question_count * 100)
    except:
        result = "N/A"
    sql = 'SELECT homework.name, class_homework.due_date ' \
          'FROM homework INNER JOIN class_homework on homework.id = class_homework.homework_id ' \
          'WHERE homework.id = ?'
    c.execute(sql, (homework_id,))
    name_and_due_date = c.fetchall()[0]
    return name_and_due_date[0], result, name_and_due_date[1]


if __name__ == '__main__':
    print(get_classes_of_user(1))
    print(get_homework_ids(486))
    print(get_homework_score(1, 486))
