import random
import sqlite3

import scripts.db_scripts

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


def user():
    identity = 1
    while identity <= 100:
        username = 'student{}'.format(identity)
        password_salt = scripts.db_scripts.generate_salt()
        password_hash = scripts.db_scripts.generate_hash('password', password_salt)
        first_name = 'first{}'.format(identity)
        last_name = 'last{}'.format(identity)
        user_type = 's'
        sql = 'INSERT INTO users(username, password_salt, password_hash, first_name, last_name, type)' \
              'VALUES(?, ?, ?, ?, ?, ?);'
        c.execute(sql, (username, password_salt, password_hash, first_name, last_name, user_type))
        identity += 1
    identity = 1
    while identity <= 100:
        username = 'teacher{}'.format(identity)
        password_salt = scripts.db_scripts.generate_salt()
        password_hash = scripts.db_scripts.generate_hash('password', password_salt)
        first_name = 'first{}'.format(identity)
        last_name = 'last{}'.format(identity)
        user_type = 't'
        sql = 'INSERT INTO users(username, password_salt, password_hash, first_name, last_name, type)' \
              'VALUES(?, ?, ?, ?, ?, ?);'
        c.execute(sql, (username, password_salt, password_hash, first_name, last_name, user_type))
        identity += 1
    conn.commit()


def classes():
    identity = 1
    while identity <= 1000:
        name = 'class{}'.format(identity)
        teacher = random.randint(101, 200)
        sql = 'INSERT INTO classes(name, teacher)' \
              'VALUES(?, ?);'
        c.execute(sql, (name, teacher))
        identity += 1
    conn.commit()


def class_user():
    identity = 1
    while identity <= 10000:
        class_id = random.randint(1, 1000)
        student_id = random.randint(1, 100)
        sql = 'INSERT INTO class_user(class_id, student_id)' \
              'VALUES(?, ?);'
        c.execute(sql, (class_id, student_id))
        identity += 1
    conn.commit()


def question_types():
    identity = 1
    while identity <= 100:
        question_type = 'type{}'.format(identity)
        sql = 'INSERT INTO question_types(type)' \
              'VALUES(?);'
        c.execute(sql, (question_type,))
        identity += 1
    conn.commit()


def homework():
    identity = 1
    while identity <= 10000:
        name = 'name{}'.format(identity)
        description = 'description{}'.format(identity)
        sql = 'INSERT INTO homework(name, description)' \
              'VALUES(?, ?);'
        c.execute(sql, (name, description))
        identity += 1
    conn.commit()


def questions():
    identity = 1
    while identity <= 100000:
        name = 'question{}'.format(identity)
        type_id = random.randint(1, 100)
        question_text = 'question text {}'.format(identity)
        correct_answer = 'correct answer {}'.format(identity)
        answer_b = 'b {}'.format(identity)
        answer_c = 'c {}'.format(identity)
        answer_d = 'd {}'.format(identity)
        sql = 'INSERT INTO questions(name, type_id, question_text, correct_answer, answer_b, answer_c, answer_d)' \
              'VALUES(?, ?, ?, ?, ?, ?, ?);'
        c.execute(sql, (name, type_id, question_text, correct_answer, answer_b, answer_c, answer_d))
        identity += 1
    conn.commit()


def homework_questions():
    identity = 1
    while identity <= 100000:
        homework_id = random.randint(1, 10000)
        question_id = identity
        sql = 'INSERT INTO homework_questions(homework_id, question_id)' \
              'VALUES(?, ?);'
        c.execute(sql, (homework_id, question_id))
        identity += 1
    conn.commit()


def class_homework():
    identity = 1
    while identity <= 10000:
        class_id = random.randint(1, 1000)
        homework_id = identity
        due_date = '{}-{}-{}'.format((random.randint(2010, 2020)), (random.randint(1, 12)), (random.randint(1, 28)))
        sql = 'INSERT INTO class_homework(class_id, homework_id, due_date)' \
              'VALUES(?, ?, ?);'
        c.execute(sql, (class_id, homework_id, due_date))
        identity += 1
    conn.commit()


def question_results():
    identity = 1
    while identity <= 100:
        user_id = identity
        sql = 'SELECT homework_questions.question_id ' \
              'FROM ((((homework_questions INNER JOIN homework ON homework.id = homework_questions.homework_id) ' \
              'INNER JOIN class_homework ON class_homework.homework_id = homework.id) ' \
              'INNER JOIN classes ON class_homework.class_id = classes.id) ' \
              'INNER JOIN class_user ON class_user.class_id = classes.id) ' \
              'INNER JOIN users ON users.id = class_user.student_id ' \
              'WHERE users.id = ?'
        c.execute(sql, (user_id,))
        question_ids = c.fetchall()
        for each_question in question_ids:
            attempts = random.randint(0, 5)
            if attempts == 0:
                correct = 'F'
            else:
                correct = random.choice(['T', 'F'])
            sql = 'INSERT INTO question_results(user_id, question_id, attempts, correct) ' \
                  'VALUES(?, ?, ?, ?)'
            c.execute(sql, (user_id, each_question[0], attempts, correct))
        identity += 1
    conn.commit()

# user()
# classes()
# class_user()
# question_types()
# homework()
# questions()
# homework_questions()
# class_homework()
# question_results()
