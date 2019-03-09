import sqlite3
import scripts.db_scripts as db_scripts
import datetime

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


def get_homework_name_and_due_date(homework_id: int, class_id: int) -> tuple:
    # Takes a homework and class id and returns the relevant name and due date from the homework and class_homework
    # tables respectively by joining all relevant tables appropriately
    sql: str = 'SELECT homework.name, class_homework.due_date ' \
               'FROM homework INNER JOIN class_homework on homework.id = class_homework.homework_id ' \
               'WHERE homework.id = ? and class_homework.class_id =?;'
    c.execute(sql, (homework_id, class_id))
    return c.fetchall()[0]


def get_homework_score(user_id: int, homework_id: int, class_id: int) -> tuple:
    # Takes a user, class and homework id, finds the results for all questions in the given homework for the given user,
    # and for each question returns a boolean value for if the question has been correctly answered and the number of
    # times that question has been attempted from the question_results table by joining all relevant tables
    # appropriately
    sql: str = 'SELECT question_results.attempts, question_results.correct ' \
               'FROM ((homework INNER JOIN homework_questions ON homework.id = homework_questions.homework_id)' \
               'INNER JOIN questions ON homework_questions.question_id = questions.id) ' \
               'INNER JOIN question_results ON questions.id = question_results.question_id ' \
               'WHERE question_results.user_id = ? AND homework.id = ?;'
    c.execute(sql, (user_id, homework_id))
    score_list: tuple = c.fetchall()
    # Iterates through each question result stored in the score list and increments the score for the homework by 1
    # divided by the number of attempts if the question was correctly answered (has 'True' in the first position of the
    # tuple). This value is rounded to the nearest integer
    # Question count is incremented each loop to get a value for the number of questions in the homework
    question_count: int = 0
    score: int = 0
    for each_score in score_list:
        question_count += 1
        if each_score[1] == 'T':
            score += (1 / each_score[0])
    # Calculates the percentage score for the homework by dividing the score by the number of questions and multiplying
    # by 100. If the homework has no questions (e.g. if the given student was never set the given homework), a division
    # by zero will occur. This is handled by simply setting a score of "N/A"
    try:
        result: int = round(score / question_count * 100)
    except ZeroDivisionError:
        result = "N/A"
    # Function to be returned to in UI also requires homework name and due date so this data is found and returned with
    # the homework result
    name_and_due_date: tuple = get_homework_name_and_due_date(homework_id, class_id)
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
    # Inserts required data for the new student into the class_user table (id of class added to and id of student being
    # added)
    sql: str = 'INSERT INTO class_user(class_id, student_id) VALUES(?, ?);'
    c.execute(sql, (class_id, student_id))
    # Inserts required data for the new student into the question_results table by finding all questions within each
    # homework already assigned to the class and creating an entry in the table for each with (student_id, id of
    # question, 0 as the number of attempts, False as the question completion status)
    sql: str = 'INSERT INTO question_results(user_id, question_id, attempts, correct) VALUES (?, ?, ?, ?)'
    for each_homework in get_homework_of_class(class_id):
        for each_question in get_questions_of_homework(each_homework[0]):
            c.execute(sql, (student_id, each_question[0], 0, 'F'))
    conn.commit()


def check_student_in_class(student_id: int, class_id: int) -> bool:
    # Finds the number of occurrences in the class_user table of the inputted student_id in the same record as the
    # given class_id. If 0 returned, relationship is not in DB (student not in class)
    sql: str = 'SELECT COUNT(1) FROM class_user WHERE class_id = ? AND student_id = ?;'
    c.execute(sql, (class_id, student_id))
    if c.fetchall()[0][0] > 0:
        return True
    else:
        return False


def remove_student_from_class(student_id: int, class_id: int):
    # Deletes any entry in class_user which links the given user to the given class
    sql: str = 'DELETE FROM class_user WHERE student_id = ? AND class_id = ?;'
    c.execute(sql, (student_id, class_id))
    conn.commit()


def create_class(teacher_id: int, class_name: str):
    # Inserts into the classes tables a new record with the new class' name and the id of the teacher who created it
    sql: str = 'INSERT INTO classes(name, teacher) VALUES(?, ?);'
    c.execute(sql, (class_name, teacher_id))
    conn.commit()


def remove_class(class_id: int):
    # Deletes all entries in each table which references the existence of the given class
    # Deletes any entry in class_user relating to the given class_id
    sql: str = 'DELETE FROM class_user WHERE class_id = ?'
    c.execute(sql, (class_id,))
    # Deletes any entry in class_homework relating to the given class_id
    sql: str = 'DELETE FROM class_homework WHERE class_id = ?'
    c.execute(sql, (class_id,))
    # Deletes any entry in classes relating to the given class_id
    sql: str = 'DELETE FROM classes WHERE id = ?;'
    c.execute(sql, (class_id,))
    conn.commit()


def get_results_of_homework(class_id: int, homework_id: int) -> list:
    # Gets list of all students in the given class so results for each student in the class can be found later
    students: list = get_students_of_class(class_id)
    scores: list = []
    # For every student in the class, the following data is found and appended as a tuple of the format
    # [first_name, last_name, score, percentage, attempts] to the list 'scores':
    for student in students:
        user_id: int = student[0]
        # Takes the user id for the current student, the id of the current class and the id of the current homework,
        # finds all question results for the given user for the given homework within the given class, and returns the
        # question correctly answered status and number of attempts for each relevant result from the question_results
        # table by joining all relevant tables appropriately. Data is stored in tuple 'results'
        sql: str = 'SELECT question_results.correct, question_results.attempts ' \
                   'FROM users INNER JOIN ((class_homework ' \
                   'INNER JOIN homework_questions ON class_homework.homework_id = homework_questions.homework_id) ' \
                   'INNER JOIN question_results ON homework_questions.question_id = question_results.question_id) ' \
                   'ON question_results.user_id = users.id ' \
                   'WHERE class_homework.class_id = ? AND class_homework.homework_id = ? AND users.id = ?'
        c.execute(sql, (class_id, homework_id, user_id))
        results: tuple = c.fetchall()
        # Gets the first and last names for the given user
        first_name: str = db_scripts.get_first_name(user_id)
        last_name: str = db_scripts.get_last_name(user_id)
        # Calculates the score as a percentage for the current user by taking the sum of the number of questions with
        # True as the correct status and dividing by the question count then multiplying by 100. The number of attempts
        # is found by iterating through each question score and setting the number of attempts variable to the number of
        # attempts for that question if it is greater than the currently stored value (finds the maximum number of
        # attempts taken across all questions for that user). If for any reason the number of questions is 0 (i.e.
        # homework has no questions), a division by zero error occurs when calculating score. As a score out of 0 cannot
        # exist anyway, this is fixed by catching a division by zero error and setting the score to 'N/A'
        score: int = 0
        attempts: int = 0
        question_count: int = 0
        correct_count: int = 0
        for question in results:
            question_count += 1
            if question[0] == 'T':
                correct_count += 1
                score += (1 / question[1])
            if question[1] > attempts:
                attempts = question[1]
        try:
            percentage: str = round(score / question_count * 100)
        except ZeroDivisionError:
            percentage: str = "N/A"
        # Appends entry for given student to scores list as a tuple of the appropriate format
        scores.append([first_name, last_name, correct_count, percentage, attempts])
    # Returns array of score data
    return scores


def get_name_of_homework(homework_id: int) -> str:
    # Returns homework name from database for given homework id
    sql: str = 'SELECT name FROM homework WHERE id = ?;'
    c.execute(sql, (homework_id,))
    return c.fetchall()[0][0]


def get_scores_of_student_in_class(class_id: int, student_id: int) -> list:
    # Gets list of all homework in the given class so results for each homework in the class can be found later
    homework: list = get_homework_of_class(class_id)
    scores: list = []
    # For every homework in the class, the following data is found and appended as a tuple of the format
    # [homework name, score, percentage, attempts] to the list 'scores':
    for homework in homework:
        homework_id = homework[0]
        # Takes the user id for the current student, the id of the current class and the id of the current homework,
        # finds all question results for the given user for the given homework within the given class, and returns the
        # question correctly answered status and number of attempts for each relevant result from the question_results
        # table by joining all relevant tables appropriately. Data is stored in tuple 'results'
        sql: str = 'SELECT question_results.correct, question_results.attempts ' \
                   'FROM users INNER JOIN ((class_homework ' \
                   'INNER JOIN homework_questions ON class_homework.homework_id = homework_questions.homework_id) ' \
                   'INNER JOIN question_results ON homework_questions.question_id = question_results.question_id) ' \
                   'ON question_results.user_id = users.id ' \
                   'WHERE class_homework.class_id = ? AND class_homework.homework_id = ? AND users.id = ?'
        c.execute(sql, (class_id, homework_id, student_id))
        results: tuple = c.fetchall()
        # Gets the name of the current homework beign analysed
        homework_name: str = get_name_of_homework(homework_id)
        # Calculates the score as a percentage for the current homeowrk by taking the sum of the number of questions
        # with True as the correct status and dividing by the question count then multiplying by 100. The number of
        # attempts is found by iterating through each question score and setting the number of attempts variable to the
        # number of attempts for that question if it is greater than the currently stored value (finds the maximum
        # number of attempts taken across all questions for that user). If for any reason the number of questions is 0
        # (i.e. homework has no questions), a division by zero error occurs when calculating score. As a score out of 0
        # cannot exist anyway, this is fixed by catching a division by zero error and setting the score to 'N/A'
        score: int = 0
        attempts: int = 0
        question_count: int = 0
        correct_count: int = 0
        for question in results:
            question_count += 1
            if question[0] == 'T':
                score += (1 / question[1])
                correct_count += 1
            if question[1] > attempts:
                attempts = question[1]
        try:
            percentage: str = round(score / question_count * 100)
        except ZeroDivisionError:
            percentage: str = "N/A"
        # Appends entry for given homework to scores list as a tuple of the appropriate format
        scores.append([homework_name, correct_count, percentage, attempts])
    # Returns array of score data
    return scores


def get_question_text_of_question(question_id: int) -> str:
    # Returns question text from database for given question id
    sql: str = 'SELECT question_text FROM questions WHERE id = ?;'
    c.execute(sql, (question_id,))
    return c.fetchall()[0][0]


def get_correct_answer_of_question(question_id: int) -> int:
    # Returns correct answer from database for given question id
    sql: str = 'SELECT correct_answer FROM questions WHERE id = ?;'
    c.execute(sql, (question_id,))
    return c.fetchall()[0][0]


def remove_question_from_homework(question_id: int, homework_id: int):
    # Deletes any entry in homework_questions which links the given question to the given homework
    sql: str = 'DELETE FROM homework_questions WHERE question_id = ? AND homework_id = ?;'
    c.execute(sql, (question_id, homework_id))
    conn.commit()


def insert_question_into_homework(class_id: int, homework_id: int, question_id: int):
    # Inserts required data to link a homework and question into the homework_questions table (id of question and id of
    # homework to be added to)
    sql: str = 'INSERT INTO homework_questions(homework_id, question_id) VALUES(?,?)'
    c.execute(sql, (homework_id, question_id))
    # Inserts required data for the new question into the question_results table by finding all students within the
    # given class and for each student inserting an entry linking the user id to the question id along with the number
    # of attempts(set initially to 0 as question unattempted) and correct status (set initially to False as question
    # unattempted)
    for user in get_students_of_class(class_id):
        sql: str = 'INSERT INTO question_results(user_id, question_id, attempts, correct) VALUES(?,?,?,?)'
        c.execute(sql, (user[0], question_id, 0, 0))
    conn.commit()


# NOT YET DOCUMENTED BEYOND HERE

def get_incorrect_answers_of_question(question_id: int) -> list:
    # Returns correct answer from database for given question id
    sql: str = 'SELECT answer_b, answer_c, answer_d FROM questions WHERE id = ?;'
    c.execute(sql, (question_id,))
    return c.fetchall()[0]


def get_correct_status_of_question(student_id: int, question_id: int) -> bool:
    sql: str = 'SELECT correct FROM question_results WHERE user_id = ? AND question_id = ?;'
    c.execute(sql, (student_id, question_id))
    if c.fetchall()[0][0] == 'T':
        return True
    else:
        return False


def increment_user_attempts_at_question(user_id: int, question_id: int):
    sql: str = 'UPDATE question_results SET attempts = attempts + 1 WHERE user_id = ? AND question_id = ?;'
    c.execute(sql, (user_id, question_id))
    conn.commit()


def mark_question_as_correct(user_id: int, question_id: int):
    sql: str = 'UPDATE question_results SET correct = ? WHERE user_id = ? AND question_id = ?;'
    c.execute(sql, ('T', user_id, question_id))
    conn.commit()


def insert_new_homework(name: str, description: str) -> int:
    sql: str = 'INSERT INTO homework(name, description) VALUES(?,?)'
    c.execute(sql, (name, description))
    homework_id: int = c.lastrowid
    conn.commit()
    return homework_id


def add_homework_to_class(class_id: int, homework_id: int, due_date: datetime.date):
    due_year_month_day: list = str(due_date).split('-')
    string_due_date: str = "{}-{}-{}".format(int(due_year_month_day[0]), int(due_year_month_day[1]),
                                             int(due_year_month_day[2]))
    sql: str = 'INSERT INTO class_homework(class_id, homework_id, due_date) VALUES(?,?,?)'
    c.execute(sql, (class_id, homework_id, string_due_date))
    conn.commit()


def remove_homework(homework_id: int):
    sql: str = 'DELETE FROM homework WHERE id = ?;'
    c.execute(sql, (homework_id,))
    sql: str = 'DELETE FROM class_homework WHERE homework_id = ?'
    c.execute(sql, (homework_id,))
    sql: str = 'DELETE FROM homework_questions WHERE homework_id = ?'
    c.execute(sql, (homework_id,))
    conn.commit()


def get_question_type(question_id: int) -> str:
    sql: str = 'SELECT question_types.type FROM question_types INNER JOIN questions ' \
               'ON question_types.id = questions.type_id WHERE questions.id = ?'
    c.execute(sql, (question_id,))
    return c.fetchall()[0][0]


if __name__ == '__main__':
    print(get_question_type(45))
