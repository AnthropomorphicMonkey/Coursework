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


def get_homeworks_of_class(class_id) -> list:
    sql = 'SELECT homework.id, homework.name ' \
          'FROM homework INNER JOIN class_homework ON homework.id = class_homework.homework_id ' \
          'WHERE class_homework.class_id = ?;'
    c.execute(sql, (class_id,))
    return c.fetchall()


def get_homework_score(user_id: int, homework_id: int) -> tuple:
    sql = 'SELECT question_results.attempts, question_results.correct ' \
          'FROM ((homework INNER JOIN homework_questions ON homework.id = homework_questions.homework_id)' \
          'INNER JOIN questions ON homework_questions.question_id = questions.id) ' \
          'INNER JOIN question_results ON questions.id = question_results.question_id ' \
          'WHERE question_results.user_id = ? AND homework.id = ?;'
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
          'WHERE homework.id = ?;'
    c.execute(sql, (homework_id,))
    name_and_due_date = c.fetchall()[0]
    return name_and_due_date[0], result, name_and_due_date[1]


def get_classes_of_teacher(user_id: int) -> list:
    sql = 'SELECT id, name FROM classes WHERE teacher = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()


def get_users_of_class(class_id: int) -> list:
    sql = 'SELECT users.id, users.username ' \
          'FROM class_user INNER JOIN users ON class_user.student_id = users.id ' \
          'WHERE class_user.class_id = ?;'
    c.execute(sql, (class_id,))
    return c.fetchall()


def get_questions_of_homework(homework_id: int) -> list:
    sql = 'SELECT questions.id, questions.name FROM ' \
          'questions INNER JOIN homework_questions ON questions.id = homework_questions.question_id ' \
          'WHERE homework_questions.homework_id = ?;'
    c.execute(sql, (homework_id,))
    return c.fetchall()


def add_user_to_class(student_id: int, class_id: int):
    sql = 'INSERT INTO class_user(class_id, student_id) VALUES(?, ?);'
    c.execute(sql, (class_id, student_id))
    sql = 'INSERT INTO question_results(user_id, question_id, attempts, correct) VALUES (?, ?, ?, ?)'
    for each_homework in get_homeworks_of_class(class_id):
        for each_question in get_questions_of_homework(each_homework[0]):
            c.execute(sql, (student_id, each_question[0], 0, 'F'))
    conn.commit()


def check_user_in_class(student_id: int, class_id: int) -> bool:
    sql = 'SELECT COUNT(1) FROM class_user WHERE class_id = ? AND student_id = ?;'
    c.execute(sql, (class_id, student_id))
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


def remove_user_from_class(student_id: int, class_id: int):
    sql = 'DELETE FROM class_user WHERE student_id = ? AND class_id = ?;'
    c.execute(sql, (student_id, class_id))
    conn.commit()


def create_class(teacher_id: int, class_name: str):
    sql = 'INSERT INTO classes(name, teacher) VALUES(?, ?);'
    c.execute(sql, (class_name, teacher_id))
    conn.commit()


if __name__ == '__main__':
    print(get_classes_of_user(1))
    print(get_homeworks_of_class(486))
    print(get_homework_score(1, 486))
    print(get_classes_of_teacher(156))
    print(get_users_of_class(1))
    print(get_questions_of_homework(4))
    print(check_user_in_class(1, 486))
