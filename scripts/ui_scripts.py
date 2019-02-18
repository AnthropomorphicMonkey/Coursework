import sqlite3
import scripts.db_scripts as db_scripts

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


def get_classes_of_student(user_id: int) -> list:
    # Takes a user id, finds all classes student is a member of, and returns the class id and name for each relevant
    # class from the classes table by joining all relevant tables appropriately
    sql: str = 'SELECT classes.id, classes.name ' \
               'FROM ((class_user INNER JOIN classes ON class_user.class_id = classes.id)' \
               'INNER JOIN users ON users.id = class_user.student_id) ' \
               'WHERE users.id = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()


def get_homework_of_class(class_id) -> list:
    # Takes a class id, finds all homework belonging to the class, and returns the homework id and name for each
    # relevant homework from the homework table by joining all relevant tables appropriately
    sql: str = 'SELECT homework.id, homework.name ' \
               'FROM homework INNER JOIN class_homework ON homework.id = class_homework.homework_id ' \
               'WHERE class_homework.class_id = ?;'
    c.execute(sql, (class_id,))
    return c.fetchall()


def get_homework_score(user_id: int, homework_id: int) -> tuple:
    sql: str = 'SELECT question_results.attempts, question_results.correct ' \
               'FROM ((homework INNER JOIN homework_questions ON homework.id = homework_questions.homework_id)' \
               'INNER JOIN questions ON homework_questions.question_id = questions.id) ' \
               'INNER JOIN question_results ON questions.id = question_results.question_id ' \
               'WHERE question_results.user_id = ? AND homework.id = ?;'
    c.execute(sql, (user_id, homework_id))
    score_list: tuple = c.fetchall()
    question_count: int = 0
    score: int = 0
    for each_score in score_list:
        question_count += 1
        if each_score[1] == 'T':
            score += (1 / each_score[0])
    try:
        result: int = round(score / question_count * 100)
    except ZeroDivisionError:
        result = "N/A"
    sql: str = 'SELECT homework.name, class_homework.due_date ' \
               'FROM homework INNER JOIN class_homework on homework.id = class_homework.homework_id ' \
               'WHERE homework.id = ?;'
    c.execute(sql, (homework_id,))
    name_and_due_date: tuple = c.fetchall()[0]
    return name_and_due_date[0], result, name_and_due_date[1]


def get_classes_of_teacher(user_id: int) -> list:
    # Takes a user id (assumed to be that of a teacher and to be verified before calling function) and returns the
    # class id and name for each relevant class from the classes table
    sql: str = 'SELECT id, name FROM classes WHERE teacher = ?;'
    c.execute(sql, (user_id,))
    return c.fetchall()


def get_students_of_class(class_id: int) -> list:
    # Takes a class id, finds all students belonging to the class, and returns the student id and name for each relevant
    # student from the users table by joining all relevant tables appropriately
    sql: str = 'SELECT users.id, users.username ' \
               'FROM class_user INNER JOIN users ON class_user.student_id = users.id ' \
               'WHERE class_user.class_id = ?;'
    c.execute(sql, (class_id,))
    return c.fetchall()


def get_questions_of_homework(homework_id: int) -> list:
    # Takes a homework id, finds all questions belonging to the homework, and returns the quesion id and name for each
    # relevant question from the questions table by joining all relevant tables appropriately
    sql: str = 'SELECT questions.id, questions.name FROM ' \
               'questions INNER JOIN homework_questions ON questions.id = homework_questions.question_id ' \
               'WHERE homework_questions.homework_id = ?;'
    c.execute(sql, (homework_id,))
    return c.fetchall()


def add_student_to_class(student_id: int, class_id: int):
    sql: str = 'INSERT INTO class_user(class_id, student_id) VALUES(?, ?);'
    c.execute(sql, (class_id, student_id))
    sql: str = 'INSERT INTO question_results(user_id, question_id, attempts, correct) VALUES (?, ?, ?, ?)'
    for each_homework in get_homework_of_class(class_id):
        for each_question in get_questions_of_homework(each_homework[0]):
            c.execute(sql, (student_id, each_question[0], 0, 'F'))
    conn.commit()


def check_student_in_class(student_id: int, class_id: int) -> bool:
    sql: str = 'SELECT COUNT(1) FROM class_user WHERE class_id = ? AND student_id = ?;'
    c.execute(sql, (class_id, student_id))
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


def remove_student_from_class(student_id: int, class_id: int):
    sql: str = 'DELETE FROM class_user WHERE student_id = ? AND class_id = ?;'
    c.execute(sql, (student_id, class_id))
    conn.commit()


def create_class(teacher_id: int, class_name: str):
    sql: str = 'INSERT INTO classes(name, teacher) VALUES(?, ?);'
    c.execute(sql, (class_name, teacher_id))
    conn.commit()


def remove_class(class_id: int):
    sql: str = 'DELETE FROM class_user WHERE class_id = ?'
    c.execute(sql, (class_id,))
    sql: str = 'DELETE FROM class_homework WHERE class_id = ?'
    c.execute(sql, (class_id,))
    sql: str = 'DELETE FROM classes WHERE id = ?;'
    c.execute(sql, (class_id,))
    conn.commit()


def get_results_of_homework(class_id: int, homework_id: int) -> list:
    students: list = get_students_of_class(class_id)
    scores: list = []
    for student in students:
        user_id: int = student[0]
        sql: str = 'SELECT question_results.correct, question_results.attempts ' \
                   'FROM users INNER JOIN ((class_homework ' \
                   'INNER JOIN homework_questions ON class_homework.homework_id = homework_questions.homework_id) ' \
                   'INNER JOIN question_results ON homework_questions.question_id = question_results.question_id) ' \
                   'ON question_results.user_id = users.id ' \
                   'WHERE class_homework.class_id = ? AND class_homework.homework_id = ? AND users.id = ?'
        c.execute(sql, (class_id, homework_id, user_id))
        results: tuple = c.fetchall()
        first_name: str = db_scripts.get_first_name(user_id)
        last_name: str = db_scripts.get_last_name(user_id)
        score: int = 0
        attempts: int = 0
        question_count: int = 0
        for question in results:
            question_count += 1
            if question[0] == 'T':
                score += 1
            if question[1] > attempts:
                attempts = question[1]
        try:
            percentage: str = round(score / question_count * 100)
        except ZeroDivisionError:
            percentage: str = "N/A"
        scores.append([first_name, last_name, score, percentage, attempts])
    return scores


def get_name_of_homework(homework_id: int):
    sql: str = 'SELECT name FROM homework WHERE id = ?;'
    c.execute(sql, (homework_id,))
    return c.fetchall()[0][0]


def get_scores_of_student_in_class(class_id: int, student_id: int):
    homeworks: list = get_homework_of_class(class_id)
    scores: list = []
    for homework in homeworks:
        homework_id = homework[0]
        sql: str = 'SELECT question_results.correct, question_results.attempts ' \
                   'FROM users INNER JOIN ((class_homework ' \
                   'INNER JOIN homework_questions ON class_homework.homework_id = homework_questions.homework_id) ' \
                   'INNER JOIN question_results ON homework_questions.question_id = question_results.question_id) ' \
                   'ON question_results.user_id = users.id ' \
                   'WHERE class_homework.class_id = ? AND class_homework.homework_id = ? AND users.id = ?'
        c.execute(sql, (class_id, homework_id, student_id))
        results: tuple = c.fetchall()
        homework_name: str = get_name_of_homework(homework_id)
        score: int = 0
        attempts: int = 0
        question_count: int = 0
        for question in results:
            question_count += 1
            if question[0] == 'T':
                score += 1
            if question[1] > attempts:
                attempts = question[1]
        try:
            percentage: str = round(score / question_count * 100)
        except ZeroDivisionError:
            percentage: str = "N/A"
        scores.append([homework_name, score, percentage, attempts])
    return scores


if __name__ == '__main__':
    hid = input("Enter homework id: ")
    print(get_questions_of_homework(hid))
