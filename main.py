# If all present, imports all modules, otherwise returns an error for 5 seconds and exits program
# noinspection SpellCheckingInspection
try:
    import sys
    from PyQt5 import QtWidgets
    from PyQt5 import uic
    from PyQt5 import QtCore
    from PyQt5 import QtChart
    # 'pyrcc5 -o window_rc.py window.qrc' Used to generate resource file (window_rc.py)
    from scripts import db_scripts, ui_scripts
    import questions.question_scripts as question_scripts
    import questions.mechanics
    import questions.calculus
    import datetime
    import random
except ModuleNotFoundError:
    try:
        import time

        print("Required modules are not installed, program requires:\n-PyQt5")
        time.sleep(5)
        raise SystemExit
    # Program simply exits immediately if even built in time library is not present
    except ModuleNotFoundError:
        raise SystemExit


# Window class to control uid
class Window(QtWidgets.QMainWindow, uic.loadUiType('window.ui')[0]):
    # <editor-fold desc="General">
    # noinspection PyArgumentList
    def __init__(self):
        # Inherits from generic window class from QT
        super().__init__()
        self.setupUi(self)
        # Declare constants related to page indexes of different sections of the program
        self.login_page: int = 0
        self.create_account_page: int = 1
        self.student_main_menu_page: int = 2
        self.teacher_main_menu_page: int = 3
        self.question_page: int = 4
        self.homework_select_page: int = 5
        self.browse_quizzes_page: int = 6
        self.previous_scores_page: int = 7
        self.set_homework_page: int = 8
        self.admin_page: int = 9
        self.account_management_page: int = 10
        self.view_classes_page: int = 11
        # Holds ID of active user
        self.current_user: int = -1
        # Clears list of user classes
        self.student_classes: list = []
        self.teacher_classes: list = []
        self.class_users: list = []
        # Sets up all pages
        self.button_setup()
        self.reset_pages(self.login_page)
        # Sets program to logged out state (and hides logged out message)
        self.logout()
        self.login_success_output.setText("")
        # Holds classes or students of currently selected class on the view classes page
        self.view_classes_students_or_homework: list = []
        self.set_homework_homework: list = []
        self.set_homework_questions: list = []
        self.homework_select_valid_homework_ids: list = []
        self.current_homework_questions: list = []
        self.question_number: int = 0
        self.correct_answer_location: int = 1
        self.class_homework: list = []

    def change_page(self, index: int):
        # Restores target page to default state
        self.reset_pages(index)
        # Enables all navigation buttons to then be disabled as needed
        self.show_main_menu_button()
        self.show_logout_button()
        # Only tries to show username if logged in
        if self.current_user != -1:
            self.show_username_text()
        # If a logged out page or menu page, hides main menu button
        if index in [0, 1, 2, 3]:
            self.hide_main_menu_button()
            # If a logged out page, hide logout button
            if index in [0, 1]:
                self.hide_logout_button()
                self.hide_username_text()
        # Changes the current page index to the value passed
        self.main_widget.setCurrentIndex(index)

    def button_setup(self):
        # Runs all button setups
        self.navigation_button_setup()
        self.login_page_button_setup()
        self.create_account_page_button_setup()
        self.student_main_menu_page_button_setup()
        self.teacher_main_menu_page_button_setup()
        self.previous_scores_page_button_setup()
        self.admin_page_button_setup()
        self.account_management_page_button_setup()
        self.view_classes_page_button_setup()
        self.set_homework_page_button_setup()
        self.homework_select_page_button_setup()
        self.question_page_button_setup()

    def reset_pages(self, target_page):
        # Runs all page reset scripts
        if target_page == self.login_page:
            self.login_reset_page()
        elif target_page == self.create_account_page:
            self.create_account_reset_page()
        elif target_page == self.question_page:
            self.question_number = 0
            self.question_reset_page()
        elif target_page == self.previous_scores_page:
            self.previous_scores_reset_page()
        elif target_page == self.admin_page:
            self.admin_reset_page()
        elif target_page == self.account_management_page:
            self.account_management_reset_page()
        elif target_page == self.view_classes_page:
            self.view_classes_reset_page()
        elif target_page == self.set_homework_page:
            self.set_homework_reset_page()
        elif target_page == self.homework_select_page:
            self.homework_select_reset_page()
        else:
            pass

    # </editor-fold>

    # <editor-fold desc="Navigation bar">
    def show_main_menu_button(self):
        # Enables and shows main menu button
        self.main_menu_button.setEnabled(True)
        self.main_menu_button.setVisible(True)

    def hide_main_menu_button(self):
        # Disables amd hides main menu button
        self.main_menu_button.setEnabled(False)
        self.main_menu_button.setVisible(False)

    def show_username_text(self):
        # Makes the user's first name show in ui
        self.username_label.setText(db_scripts.get_first_name(self.current_user).title())

    def hide_username_text(self):
        # Stops showing the user's first name in ui
        self.username_label.setText("")

    def show_logout_button(self):
        # Enables and shows logout button
        self.logout_button.setEnabled(True)
        self.logout_button.setVisible(True)

    def hide_logout_button(self):
        # Disables and hides the logout button
        self.logout_button.setEnabled(False)
        self.logout_button.setVisible(False)

    def navigation_button_setup(self):
        # If logout button clicked runs logout scripts
        self.logout_button.clicked.connect(self.logout)
        self.main_menu_button.clicked.connect(self.go_to_main_menu)

    def go_to_main_menu(self):
        # Returns to the correct main menu page for the given user
        if db_scripts.get_account_type(self.current_user) == 't':
            self.change_page(self.teacher_main_menu_page)
        elif db_scripts.get_account_type(self.current_user) == 's':
            self.change_page(self.student_main_menu_page)
        # If data in DB is for some reason invalid, user is logged out and error shown
        else:
            self.logout()
            self.login_success_output.setText("User type error, user has been logged out")

    def logout(self):
        # Resets current user to a default value
        self.current_user: int = -1
        # Returns to login page and sets logout success message
        self.change_page(self.login_page)
        self.login_success_output.setText("Logout successful")

    # </editor-fold>

    # <editor-fold desc="Login Page">
    def login_page_button_setup(self):
        # If login submit button clicked runs scripts to verify login
        self.login_submit_button.clicked.connect(self.login)
        # If create account clicked runs scripts to change screen
        # Error passing arguments fixed using https://stackoverflow.com/questions/45793966/clicked-connect-error
        self.login_create_account_button.clicked.connect(lambda: self.change_page(self.create_account_page))

    def login_reset_page(self):
        # Sets input boxes to blank
        self.login_username_input.setText("")
        self.login_password_input.setText("")
        # Sets output labels to blank
        self.login_success_output.setText("")

    def login(self):
        # Checks if username exists (case fold used to make username case insensitive even for characters such as ß)
        if db_scripts.check_user_exists(self.login_username_input.text().casefold()):
            # Checks if password is correct
            user_id: int = db_scripts.get_user_id(self.login_username_input.text().casefold())
            if db_scripts.check_password(user_id, self.login_password_input.text()):
                # Checks user type to decide which main menu to load
                if db_scripts.get_account_type(user_id) in ['s', 't']:
                    self.login_success_output.setText("Success")
                    self.current_user: int = user_id
                    # Main menu loaded
                    self.go_to_main_menu()
                # If the stored user type is for some reason invalid, login is cancelled and error shown
                else:
                    self.login_success_output.setText("User type error")
            # If password incorrect, invalid password error is displayed and password box is cleared
            else:
                self.login_success_output.setText("Invalid password")
                self.login_password_input.setText("")
        # If username did not exist, invalid username error is displayed
        else:
            self.login_success_output.setText("Invalid username")
            self.login_username_input.setText("")

    # </editor-fold>

    # <editor-fold desc="Create Account Page">
    def create_account_page_button_setup(self):
        # If create account submit button clicked runs scripts to create account
        self.create_account_submit_button.clicked.connect(self.create_account_create_account)
        # If return to login clicked runs scripts to change screen
        self.create_account_login_button.clicked.connect(lambda: self.change_page(self.login_page))

    # </editor-fold>

    # <editor-fold desc="Student Main Menu Page">
    def student_main_menu_page_button_setup(self):
        # If browse quizzes clicked runs scripts to change screen
        self.student_main_menu_browse_quizzes_button.clicked.connect(lambda: self.change_page(self.browse_quizzes_page))
        # If homework clicked runs scripts to change screen
        self.student_main_menu_homework_button.clicked.connect(lambda: self.change_page(self.homework_select_page))
        # If previous scores clicked runs scripts to change screen
        self.student_main_menu_previous_scores_button.clicked.connect(
            lambda: self.change_page(self.previous_scores_page))
        # If account management clicked runs scripts to change screen
        self.student_main_menu_account_management_button.clicked.connect(
            lambda: self.change_page(self.account_management_page))

    # </editor-fold>

    # <editor-fold desc="Teacher Main Menu Page">
    def teacher_main_menu_page_button_setup(self):
        # If 'set homework' clicked runs scripts to change screen
        self.teacher_main_menu_set_homework_button.clicked.connect(lambda: self.change_page(self.set_homework_page))
        # If 'view classes' clicked runs scripts to change screen
        self.teacher_main_menu_view_classes_button.clicked.connect(lambda: self.change_page(self.view_classes_page))
        # If 'account management' clicked runs scripts to change screen
        self.teacher_main_menu_account_management_button.clicked.connect(
            lambda: self.change_page(self.account_management_page))
        # If 'admin' clicked runs scripts to change screen
        self.teacher_main_menu_admin_button.clicked.connect(
            lambda: self.change_page(self.admin_page))

    # </editor-fold>

    # <editor-fold desc="Question Page">
    def question_reset_page(self):
        question_id = self.current_homework_questions[self.question_number][0]
        self.question_radio_a.setChecked(True)
        self.question_topic_output.setText("")
        self.question_topic_output.setText(ui_scripts.get_question_type(question_id))
        self.question_question_output.setText(ui_scripts.get_question_text_of_question(question_id))
        correct_answer: str = ui_scripts.get_correct_answer_of_question(question_id)
        incorrect_answers: list = ui_scripts.get_incorrect_answers_of_question(question_id)
        random.shuffle(list(incorrect_answers))
        self.correct_answer_location: int = random.randint(1, 4)
        if self.correct_answer_location == 1:
            self.question_radio_a.setText(correct_answer)
            self.question_radio_b.setText(incorrect_answers[0])
            self.question_radio_c.setText(incorrect_answers[1])
            self.question_radio_d.setText(incorrect_answers[2])
        elif self.correct_answer_location == 2:
            self.question_radio_b.setText(correct_answer)
            self.question_radio_a.setText(incorrect_answers[0])
            self.question_radio_c.setText(incorrect_answers[1])
            self.question_radio_d.setText(incorrect_answers[2])
        elif self.correct_answer_location == 3:
            self.question_radio_c.setText(correct_answer)
            self.question_radio_b.setText(incorrect_answers[0])
            self.question_radio_a.setText(incorrect_answers[1])
            self.question_radio_d.setText(incorrect_answers[2])
        elif self.correct_answer_location == 4:
            self.question_radio_d.setText(correct_answer)
            self.question_radio_b.setText(incorrect_answers[0])
            self.question_radio_c.setText(incorrect_answers[1])
            self.question_radio_a.setText(incorrect_answers[2])
        self.question_feedback_output.setText("")
        if ui_scripts.get_correct_status_of_question(self.current_user, question_id):
            if self.correct_answer_location == 1:
                self.question_radio_a.setChecked(True)
            elif self.correct_answer_location == 2:
                self.question_radio_b.setChecked(True)
            elif self.correct_answer_location == 3:
                self.question_radio_c.setChecked(True)
            elif self.correct_answer_location == 4:
                self.question_radio_d.setChecked(True)
            self.question_submit_button.setEnabled(False)
            self.question_radio_a.setEnabled(False)
            self.question_radio_b.setEnabled(False)
            self.question_radio_c.setEnabled(False)
            self.question_radio_d.setEnabled(False)
            self.question_feedback_output.setText("Correct")
        else:
            self.question_submit_button.setEnabled(True)
            self.question_feedback_output.setText("")
        if self.question_number == 0:
            self.question_previous_question_button.setEnabled(False)
            self.question_previous_question_button.setVisible(False)
        else:
            self.question_previous_question_button.setEnabled(True)
            self.question_previous_question_button.setVisible(True)
        if self.question_number >= len(self.current_homework_questions) - 1:
            self.question_next_question_button.setEnabled(False)
            self.question_next_question_button.setVisible(False)
        else:
            self.question_next_question_button.setEnabled(True)
            self.question_next_question_button.setVisible(True)
        # EXPERIMENTAL
        self.chart_setup('CHART!')

    def question_page_button_setup(self):
        self.question_previous_question_button.clicked.connect(lambda: self.question_page_previous_page())
        self.question_next_question_button.clicked.connect(lambda: self.question_page_next_page())
        self.question_submit_button.clicked.connect(lambda: self.question_page_submit_response())

    def question_page_next_page(self):
        self.question_number += 1
        self.question_reset_page()

    def question_page_previous_page(self):
        self.question_number -= 1
        self.question_reset_page()

    def question_page_submit_response(self):
        question_id = self.current_homework_questions[self.question_number][0]
        ui_scripts.increment_user_attempts_at_question(self.current_user, question_id)

        if (self.correct_answer_location == 1 and self.question_radio_a.isChecked()) or (
                self.correct_answer_location == 2 and self.question_radio_b.isChecked()) or (
                self.correct_answer_location == 3 and self.question_radio_c.isChecked()) or (
                self.correct_answer_location == 4 and self.question_radio_d.isChecked()):
            ui_scripts.mark_question_as_correct(self.current_user, question_id)
            self.question_submit_button.setEnabled(False)
            self.question_feedback_output.setText("Correct")
        else:
            self.question_submit_button.setEnabled(True)
            self.question_feedback_output.setText("Incorrect")

    def chart_setup(self, title: str):
        return
        self.question_chart.setTitle(title)

    # </editor-fold>

    # <editor-fold desc="Set Homework Page">
    def set_homework_page_button_setup(self):
        self.set_homework_class_combo_box.currentIndexChanged.connect(lambda: self.set_homework_class_change())
        self.set_homework_homework_combo_box.currentIndexChanged.connect(lambda: self.set_homework_homework_change())
        self.set_homework_question_combo_box.currentIndexChanged.connect(lambda: self.set_homework_question_change())
        self.set_homework_remove_question_button.clicked.connect(lambda: self.set_homework_remove_question())
        self.set_homework_add_custom_question_button.clicked.connect(lambda: self.set_homework_add_custom_question())
        self.set_homework_add_automatic_question_button.clicked.connect(
            lambda: self.set_homework_add_automatic_question())
        self.set_homework_tab_widget.currentChanged.connect(lambda: self.set_homework_reset_labels())

    def set_homework_class_change(self):
        self.set_homework_homework_combo_box.clear()
        self.set_homework_homework: list = []
        if len(self.teacher_classes) > 0:
            self.set_homework_homework: list = ui_scripts.get_homework_of_class(
                self.teacher_classes[self.set_homework_class_combo_box.currentIndex()][0])
            for each_homework in self.set_homework_homework:
                self.set_homework_homework_combo_box.addItem(each_homework[1])
        self.set_homework_homework_change()

    def set_homework_homework_change(self):
        self.set_homework_question_combo_box.clear()
        self.set_homework_questions: list = []
        if len(self.set_homework_homework) > 0:
            self.set_homework_questions: list = ui_scripts.get_questions_of_homework(
                self.set_homework_homework[self.set_homework_homework_combo_box.currentIndex()][0])
            for each_question in self.set_homework_questions:
                self.set_homework_question_combo_box.addItem(each_question[1])
        self.set_homework_auto_question_added_output.setText("")
        self.set_homework_custom_question_added_output.setText("")
        self.set_homework_question_change()

    def set_homework_question_change(self):
        self.set_homework_removed_output.setText("")
        if len(self.set_homework_questions) > 0:
            question_id = self.set_homework_questions[self.set_homework_question_combo_box.currentIndex()][0]
            self.set_homework_question_label.setText(ui_scripts.get_question_text_of_question(question_id))
            self.set_homework_answer_label.setText(ui_scripts.get_correct_answer_of_question(question_id))
        else:
            self.set_homework_question_label.setText("")
            self.set_homework_answer_label.setText("")

    def set_homework_remove_question(self):
        if len(self.set_homework_questions) > 0:
            question_id = self.set_homework_questions[self.set_homework_question_combo_box.currentIndex()][0]
            homework_id = self.set_homework_homework[self.set_homework_homework_combo_box.currentIndex()][0]
            ui_scripts.remove_question_from_homework(question_id, homework_id)
            self.set_homework_homework_change()
            self.set_homework_removed_output.setText("Question removed")
        else:
            self.set_homework_removed_output.setText("No question to remove")

    def set_homework_reset_labels(self):
        self.set_homework_question_input.setText("")
        self.set_homework_correct_answer_input.setText("")
        self.set_homework_answer_b_input.setText("")
        self.set_homework_answer_c_input.setText("")
        self.set_homework_answer_d_input.setText("")
        self.set_homework_auto_question_added_output.setText("")
        self.set_homework_custom_question_added_output.setText("")
        self.set_homework_removed_output.setText("")
        self.set_homework_question_name_input.setText("")

    def set_homework_reset_page(self):
        self.set_homework_class_combo_box.clear()
        self.set_homework_homework_combo_box.clear()
        self.set_homework_question_combo_box.clear()
        self.set_homework_question_label.setText("")
        self.set_homework_answer_label.setText("")
        self.set_homework_reset_labels()
        self.teacher_classes: list = ui_scripts.get_classes_of_teacher(self.current_user)
        for each_class in self.teacher_classes:
            self.set_homework_class_combo_box.addItem(each_class[1])

    def set_homework_add_custom_question(self):
        if len(self.teacher_classes) == 0 or len(self.set_homework_homework) == 0:
            self.set_homework_custom_question_added_output.setText("No homework selected")
            return
        self.set_homework_custom_question_added_output.setText("")
        if self.set_homework_question_name_input.text() == "":
            self.set_homework_custom_question_added_output.setText("No question name entered")
            return
        if self.set_homework_question_input.toPlainText() == "":
            self.set_homework_custom_question_added_output.setText("No question text entered")
            return
        if self.set_homework_correct_answer_input.toPlainText() == "":
            self.set_homework_custom_question_added_output.setText("Correct answer required")
            return
        if self.set_homework_answer_b_input.toPlainText() == "":
            self.set_homework_custom_question_added_output.setText("Incorrect answer 1 required")
            return
        if self.set_homework_answer_b_input.toPlainText() == self.set_homework_correct_answer_input.toPlainText():
            self.set_homework_custom_question_added_output.setText("Answer choices cannot match")
            return
        if self.set_homework_answer_c_input.toPlainText() == "":
            answer_c = None
        else:
            if self.set_homework_answer_c_input.toPlainText() in [self.set_homework_correct_answer_input.toPlainText(),
                                                                  self.set_homework_answer_b_input.toPlainText()]:
                self.set_homework_custom_question_added_output.setText("Answer choices cannot match")
                return
            answer_c = self.set_homework_answer_c_input.toPlainText()
        if self.set_homework_answer_d_input.toPlainText() == "":
            answer_d = None
        else:
            if self.set_homework_answer_d_input.toPlainText() in [self.set_homework_correct_answer_input.toPlainText(),
                                                                  self.set_homework_answer_b_input.toPlainText(),
                                                                  self.set_homework_answer_c_input.toPlainText()]:
                self.set_homework_custom_question_added_output.setText("Answer choices cannot match")
                return
            answer_d = self.set_homework_answer_d_input.toPlainText()
        if len(self.teacher_classes) <= 0:
            self.set_homework_custom_question_added_output.setText("No class selected")
            return
        if len(self.set_homework_homework) <= 0:
            self.set_homework_custom_question_added_output.setText("No homework selected")
            return
        question = question_scripts.Question(self.set_homework_question_name_input.text().casefold(), 1, 1,
                                             self.set_homework_question_input.toPlainText(),
                                             self.set_homework_correct_answer_input.toPlainText(),
                                             self.set_homework_answer_b_input.toPlainText(), answer_c, answer_d)
        question_position: int = (question.save_question())
        ui_scripts.insert_question_into_homework(
            self.teacher_classes[self.set_homework_class_combo_box.currentIndex()][0],
            self.set_homework_homework[self.set_homework_homework_combo_box.currentIndex()][0], question_position)
        self.set_homework_homework_change()
        self.set_homework_custom_question_added_output.setText("Question Added")

    def set_homework_add_automatic_question(self):
        if len(self.teacher_classes) == 0 or len(self.set_homework_homework) == 0:
            self.set_homework_auto_question_added_output.setText("No homework selected")
            return
        self.set_homework_auto_question_added_output.setText("")
        if self.set_homework_type_combo_box.currentIndex() == 0:
            question: question_scripts.Question = questions.mechanics.find_resultant_of_two_forces(
                self.set_homework_difficulty_combo_box.currentIndex() + 1)
        elif self.set_homework_type_combo_box.currentIndex() == 1:
            question: question_scripts.Question = questions.calculus.simpsons_rule(
                self.set_homework_difficulty_combo_box.currentIndex() + 1)
        elif self.set_homework_type_combo_box.currentIndex() == 2:
            question: question_scripts.Question = questions.calculus.trapezium_rule(
                self.set_homework_difficulty_combo_box.currentIndex() + 1)
        else:
            raise IndexError
        question_position: int = (question.save_question())
        ui_scripts.insert_question_into_homework(
            self.teacher_classes[self.set_homework_class_combo_box.currentIndex()][0],
            self.set_homework_homework[self.set_homework_homework_combo_box.currentIndex()][0], question_position)
        self.set_homework_homework_change()
        self.set_homework_auto_question_added_output.setText("Question Added")
        return

    # </editor-fold>

    # <editor-fold desc="Create Account Page">
    def create_account_reset_page(self):
        # Sets radios to default selection
        self.create_account_radio_student.setChecked(True)
        # Sets input boxes to blank
        self.create_account_first_name_input.setText("")
        self.create_account_last_name_input.setText("")
        self.create_account_username_input.setText("")
        self.create_account_password_input.setText("")
        self.create_account_password_verify_input.setText("")
        # Sets output labels to blank
        self.create_account_success_output.setText("")

    def create_account_create_account(self):
        # Various error checks before creating account (error type is outputted in a label):
        # Error if username field is blank
        if self.create_account_username_input.text() == '':
            self.create_account_success_output.setText("Invalid username")
        # Error if username already taken
        elif db_scripts.check_user_exists(self.create_account_username_input.text().casefold()):
            self.create_account_success_output.setText("User already exists")
        # Error if no first name entered
        elif self.create_account_first_name_input.text() == '' or len(
                self.create_account_first_name_input.text()) > 100:
            self.create_account_success_output.setText("Invalid first name")
        # Error if no last name is entered
        elif self.create_account_last_name_input.text() == '' or len(self.create_account_last_name_input.text()) > 100:
            self.create_account_success_output.setText("Invalid last name")
        # Error if password too short
        elif len(self.create_account_password_input.text()) < 8:
            self.create_account_success_output.setText("Invalid password (Must be at least 8 characters)")
        # Error if different password entered into second password box
        elif self.create_account_password_input.text() != self.create_account_password_verify_input.text():
            self.create_account_success_output.setText("Passwords do not match")
        # Error if account type not selected
        elif not ((self.get_account_type_selected() == 's') or (self.get_account_type_selected() == 't')):
            self.create_account_success_output.setText("Account type not selected")
        # If passes all validation, account is created
        else:
            # Passes all relevant data into create account function
            db_scripts.create_account(self.create_account_username_input.text().casefold(),
                                      self.create_account_password_input.text(),
                                      self.create_account_first_name_input.text(),
                                      self.create_account_last_name_input.text(),
                                      self.get_account_type_selected())
            # Resets create account page once account successfully created
            self.reset_pages(self.create_account_page)
            # Account creation success outputted
            self.create_account_success_output.setText("Account created")

    def get_account_type_selected(self) -> str:
        # Returns whether student or teacher is selected (or neither, though this should never occur)
        if self.create_account_radio_student.isChecked():
            return 's'
        elif self.create_account_radio_teacher.isChecked():
            return 't'
        else:
            return ''

    # </editor-fold>

    # <editor-fold desc="Previous Scores Page">
    def previous_scores_reset_page(self):
        # Clears class selection combo box
        self.previous_scores_class_combo_box.clear()
        # Inserts class list into combo box
        self.student_classes: list = ui_scripts.get_classes_of_student(self.current_user)
        for each_class in self.student_classes:
            self.previous_scores_class_combo_box.addItem(each_class[1])
        # Updates score table to first class selected
        self.previous_scores_update_table()

    def previous_scores_page_button_setup(self):
        # When selected class is changed, score table is updated
        self.previous_scores_class_combo_box.currentIndexChanged.connect(lambda: self.previous_scores_update_table())

    def previous_scores_update_table(self):
        # Clears table to allow for new values
        self.previous_scores_table.clearContents()
        # If user is any classes, populates table with homework scores
        if len(self.student_classes) != 0:
            homework_ids: list = []
            # For selected, id of every homework is appended to an array
            for each_homework in ui_scripts.get_homework_of_class(
                    self.student_classes[self.previous_scores_class_combo_box.currentIndex()][0]):
                homework_ids.append(each_homework[0])
            # Inserts all homework data for class into table
            self.previous_scores_table.setRowCount(len(homework_ids))
            row_counter: int = -1
            for each_homework in homework_ids:
                row_counter += 1
                data: tuple = ui_scripts.get_homework_score(self.current_user, each_homework, self.student_classes[
                    self.previous_scores_class_combo_box.currentIndex()][0])
                self.previous_scores_table.setItem(row_counter, 0, QtWidgets.QTableWidgetItem(data[0]))
                self.previous_scores_table.setItem(row_counter, 1, QtWidgets.QTableWidgetItem("{}%".format(data[1])))
                self.previous_scores_table.setItem(row_counter, 2, QtWidgets.QTableWidgetItem(data[2]))

    # </editor-fold>

    # <editor-fold desc="Admin Page">
    def admin_clear_labels(self):
        # Sets input boxes to blank
        self.admin_username_input.setText("")
        self.admin_class_input.setText("")
        self.admin_homework_name_input.setText("")
        # Sets status outputs to blank
        self.admin_add_user_status_label.setText("")
        self.admin_remove_user_status_label.setText("")
        self.admin_create_class_status_label.setText("")
        self.admin_delete_class_status_label.setText("")
        self.admin_add_homework_status_output.setText("")
        self.admin_remove_homework_status_label.setText("")

    def admin_reset_page(self):
        # Resets all combo boxes to contain no values
        self.admin_class_user_combo_box.clear()
        self.admin_delete_class_combo_box.clear()
        # Updates combo boxes to contain relevant values for current user
        self.teacher_classes: list = ui_scripts.get_classes_of_teacher(self.current_user)
        for each_class in self.teacher_classes:
            self.admin_class_user_combo_box.addItem(each_class[1])
            self.admin_delete_class_combo_box.addItem(each_class[1])
        self.admin_update_username_combo_box()
        self.admin_update_remove_homework_combo_box()
        # Sets all labels to default values
        self.admin_clear_labels()
        # Sets valid range of dates for setting homework and default date to next day
        # noinspection PyArgumentList
        self.admin_due_date_calendar.setMinimumDate(QtCore.QDate.currentDate().addDays(1))
        # noinspection PyArgumentList
        self.admin_due_date_calendar.setSelectedDate(QtCore.QDate.currentDate().addDays(1))

    # noinspection SpellCheckingInspection
    def admin_page_button_setup(self):
        # If class selection changed, changes usernames shown in username combo box and homework shown in remove
        # homework combo box to those in new class
        self.admin_class_user_combo_box.currentIndexChanged.connect(
            lambda: self.admin_class_user_combo_box_selection_change())
        # If add user to class clicked runs scripts to add user to the class
        self.admin_username_submit_button.clicked.connect(lambda: self.admin_add_user_to_class())
        # If create class clicked runs scripts to create a new class
        self.admin_create_class_submit_button.clicked.connect(lambda: self.admin_create_class())
        # If remove user clicked runs scripts to remove a user from a class
        self.admin_remove_user_button.clicked.connect(lambda: self.admin_remove_user_from_class())
        # If remove class clicked runs scripts to delete class
        self.admin_remove_class_button.clicked.connect(lambda: self.admin_remove_class())
        # If add homework clicked runs scripts to create new homework for class
        self.admin_add_homework_button.clicked.connect(lambda: self.admin_create_homework())
        # If remove homework clicked runs scripts to remove homework from database
        self.admin_remove_homework_button.clicked.connect(lambda: self.admin_remove_homework())
        # If tab changed rests inputs and outputs
        self.admin_tab_widget.currentChanged.connect(lambda: self.admin_clear_labels())

    def admin_update_username_combo_box(self):
        # Clears class users combo box
        self.admin_username_combo_box.clear()
        # If a class is selected, stores all user ids in a list anf adds each corresponding username to the combo box
        if len(self.teacher_classes) != 0:
            self.class_users: list = ui_scripts.get_students_of_class(
                self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0])
            for each_user in self.class_users:
                self.admin_username_combo_box.addItem(each_user[1])

    def admin_update_remove_homework_combo_box(self):
        self.admin_remove_homework_combo_box.clear()
        if len(self.teacher_classes) != 0:
            self.class_homework: list = ui_scripts.get_homework_of_class(
                self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0])
            for each_homework in self.class_homework:
                self.admin_remove_homework_combo_box.addItem(each_homework[1])

    def admin_class_user_combo_box_selection_change(self):
        self.admin_update_username_combo_box()
        self.admin_update_remove_homework_combo_box()

    def admin_add_user_to_class(self):
        user: str = self.admin_username_input.text()
        # Stops scripts being able to run if the teacher has no classes to add a student to
        if len(self.teacher_classes) > 0:
            # If username exists runs scripts to add user to class
            if db_scripts.check_user_exists(user):
                user_id: int = db_scripts.get_user_id(user)
                class_id: int = self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0]
                # If user already in class outputs error
                if ui_scripts.check_student_in_class(user_id, class_id):
                    self.admin_add_user_status_label.setText("User already in class")
                # If user not already in class runs scripts to add to class and outputs success message when done
                else:
                    ui_scripts.add_student_to_class(user_id, class_id)
                    self.admin_reset_page()
                    self.admin_add_user_status_label.setText("Success")
            # If username does not exist outputs error
            else:
                self.admin_clear_labels()
                self.admin_add_user_status_label.setText("User does not exist")
        # Clears input box
        self.admin_username_input.setText("")

    def admin_remove_user_from_class(self):
        # Stops scripts being able to run if a student and/or class is not selected
        if len(self.class_users) > 0 and len(self.teacher_classes) > 0:
            # Gets the currently selected user and class and runs scripts to remove user from the class
            user_id: int = self.class_users[self.admin_username_combo_box.currentIndex()][0]
            class_id: int = self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0]
            ui_scripts.remove_student_from_class(user_id, class_id)
            # Outputs success message
            self.admin_reset_page()
            self.admin_remove_user_status_label.setText("Success")
        # If student and/or class not selected outputs error
        else:
            self.admin_clear_labels()
            self.admin_remove_user_status_label.setText("Select class and user")

    def admin_create_class(self):
        # If a name is entered for the class runs scripts to set it up in database and outputs success message when done
        if self.admin_class_input.text() != '':
            ui_scripts.create_class(self.current_user, self.admin_class_input.text())
            self.admin_reset_page()
            self.admin_create_class_status_label.setText("Success")
        # If no class name is entered outputs error
        else:
            self.admin_clear_labels()
            self.admin_create_class_status_label.setText("Class must have name")

    def admin_remove_class(self):
        # If there are no classes to select does not attempt to remove class
        if len(self.teacher_classes) > 0:
            # Runs scripts to remove class from database
            ui_scripts.remove_class(self.teacher_classes[self.admin_delete_class_combo_box.currentIndex()][0])
            self.admin_reset_page()
            # Outputs success message
            self.admin_delete_class_status_label.setText("Success")
        # If no class selected outputs error
        else:
            self.admin_reset_page()
            self.admin_delete_class_status_label.setText("No class selected")

    def admin_create_homework(self):
        if len(self.teacher_classes) > 0:
            due_date: datetime.date = datetime.date(self.admin_due_date_calendar.selectedDate().year(),
                                                    self.admin_due_date_calendar.selectedDate().month(),
                                                    self.admin_due_date_calendar.selectedDate().day())
            if self.admin_homework_name_input.text() == "":
                self.admin_add_homework_status_output.setText("Homework name required")
            elif self.admin_homework_description_input.toPlainText() == "":
                self.admin_add_homework_status_output.setText("Homework description required")
            elif due_date <= datetime.date.today():
                self.admin_add_homework_status_output.setText("Homework due date must be in the future")
            else:
                homework_id: int = ui_scripts.insert_new_homework(self.admin_homework_name_input.text(),
                                                                  self.admin_homework_description_input.toPlainText())
                ui_scripts.add_homework_to_class(
                    self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0], homework_id, due_date)
                self.admin_add_homework_status_output.setText("Homework Added")
                self.admin_homework_name_input.setText("")
                self.admin_homework_description_input.setText("")
                # noinspection PyArgumentList
                self.admin_due_date_calendar.setMinimumDate(QtCore.QDate.currentDate().addDays(1))
                # noinspection PyArgumentList
                self.admin_due_date_calendar.setSelectedDate(QtCore.QDate.currentDate().addDays(1))
        else:
            self.admin_add_homework_status_output.setText("Class must be selected")

    def admin_remove_homework(self):
        if len(self.class_homework) > 0:
            ui_scripts.remove_homework(self.class_homework[self.admin_remove_homework_combo_box.currentIndex()][0])
            self.admin_update_remove_homework_combo_box()
            self.admin_remove_homework_status_label.setText("Homework removed")
        else:
            self.admin_remove_homework_status_label.setText("Class has no homework")

    # </editor-fold>

    # <editor-fold desc="Account Management Page">
    def account_management_reset_page(self):
        # Sets input boxes to blank
        self.account_management_first_name_input.setText("")
        self.account_management_last_name_input.setText("")
        self.account_management_old_password_input.setText("")
        self.account_management_new_password_input.setText("")
        self.account_management_new_password_verify_input.setText("")
        self.account_management_success_output.setText("")

    def account_management_page_button_setup(self):
        # If submit clicked runs scripts to update user details
        self.account_management_submit_button.clicked.connect(lambda: self.account_management_detail_update())

    def account_management_detail_update(self):
        # User details will only update if current password is correct
        if db_scripts.check_password(self.current_user, self.account_management_old_password_input.text()):
            # If a potential new password is entered, runs scripts to validate
            if (self.account_management_new_password_input.text() != ''
                    or self.account_management_new_password_verify_input.text() != ''):
                # If new password and new password verification match goes to scripts to validate new password
                if (self.account_management_new_password_input.text()
                        == self.account_management_new_password_verify_input.text()):
                    # If new password is invalid outputs error
                    if len(self.account_management_new_password_input.text()) < 8:
                        self.account_management_reset_page()
                        self.account_management_success_output.setText(
                            "Invalid password (Must be at least 8 characters)")
                    # If new password entered is valid updates user data
                    else:
                        # Updates first and last names using function
                        self.account_management_update_first_and_last_names()
                        # Generates new hashed password and stores
                        db_scripts.update_password(self.current_user,
                                                   self.account_management_new_password_input.text())
                        # Outputs success
                        self.account_management_reset_page()
                        self.account_management_success_output.setText("Success")
                # If new password and verification mismatch outputs error
                else:
                    self.account_management_reset_page()
                    self.account_management_success_output.setText("New password fields must match")
            # If no new password is entered runs scripts to update first and last name
            else:
                first_or_last_updated: bool = self.account_management_update_first_and_last_names()
                self.account_management_reset_page()
                # If any data was updated outputs a success message
                if first_or_last_updated:
                    self.account_management_success_output.setText("Success")
                # If no changes were made no output
                else:
                    self.account_management_success_output.setText("")
        # If current password incorrect outputs and error
        else:
            self.account_management_reset_page()
            self.account_management_success_output.setText("Correct current password required to change user data")

    def account_management_update_first_and_last_names(self) -> bool:
        # Updating of first and last names placed in own function
        # as there are multiple routes to needing to do this in account_management_detail_update function
        # Boolean value stored and returned to indicate if any values were updated
        # in order to be able to determine if a success message should be shown in account_management_detail_update
        value_updated: bool = False
        # If a new first name was entered, value is updated in db for current user
        if self.account_management_first_name_input.text() != '':
            db_scripts.update_first_name(self.current_user, self.account_management_first_name_input.text())
            # Value updated marked as true
            value_updated: bool = True
        # If a new last name was entered, value is updated in db for current user
        if self.account_management_last_name_input.text() != '':
            db_scripts.update_last_name(self.current_user, self.account_management_last_name_input.text())
            # Value updated marked as true
            value_updated: bool = True
        # Returns whether a first an/or last name update occurred
        return value_updated

    # </editor-fold>

    # <editor-fold desc="View Classes Page">
    def view_classes_reset_page(self):
        self.view_classes_view_type_combo_box.setCurrentIndex(0)
        self.view_classes_class_combo_box.clear()
        self.teacher_classes: list = ui_scripts.get_classes_of_teacher(self.current_user)
        for each_class in self.teacher_classes:
            self.view_classes_class_combo_box.addItem(each_class[1])

    def view_classes_page_button_setup(self):
        self.view_classes_view_type_combo_box.currentIndexChanged.connect(
            lambda: self.view_classes_class_or_type_change())
        self.view_classes_class_combo_box.currentIndexChanged.connect(lambda: self.view_classes_class_or_type_change())
        self.view_classes_homework_or_student_combo_box.currentIndexChanged.connect(
            lambda: self.view_classes_update_table())

    def view_classes_class_or_type_change(self):
        self.view_classes_homework_or_student_combo_box.clear()
        self.view_classes_students_or_homework: list = []
        if len(self.teacher_classes) > 0:
            if self.view_classes_view_type_combo_box.currentIndex() == 0:
                self.view_classes_display_type_output.setText("Homework:")
                for each_homework in ui_scripts.get_homework_of_class(
                        self.teacher_classes[self.view_classes_class_combo_box.currentIndex()][0]):
                    self.view_classes_students_or_homework.append(each_homework[0])
                    self.view_classes_homework_or_student_combo_box.addItem(each_homework[1])
            else:
                self.view_classes_display_type_output.setText("Student:")
                for each_student in ui_scripts.get_students_of_class(
                        self.teacher_classes[self.view_classes_class_combo_box.currentIndex()][0]):
                    self.view_classes_students_or_homework.append(each_student[0])
                    self.view_classes_homework_or_student_combo_box.addItem(each_student[1])

    def view_classes_update_table(self):
        self.view_classes_score_table.clear()
        current_class: int = self.teacher_classes[self.view_classes_class_combo_box.currentIndex()][0]
        current_student_or_homework: int = self.view_classes_students_or_homework[
            self.view_classes_homework_or_student_combo_box.currentIndex()]
        if self.view_classes_view_type_combo_box.currentIndex() == 0:
            self.view_classes_score_table.setColumnCount(5)
            self.view_classes_score_table.setHorizontalHeaderLabels(
                ["First Name", "Last Name", "Score", "Percentage", "Attempts"])
            scores: list = ui_scripts.get_results_of_homework(current_class, current_student_or_homework)
            self.view_classes_score_table.setRowCount(len(scores))
            if len(scores) != 0:
                row_counter: int = -1
                for each_score in scores:
                    row_counter += 1
                    self.view_classes_score_table.setItem(row_counter, 0, QtWidgets.QTableWidgetItem(each_score[0]))
                    self.view_classes_score_table.setItem(row_counter, 1, QtWidgets.QTableWidgetItem(each_score[1]))
                    self.view_classes_score_table.setItem(row_counter, 2,
                                                          QtWidgets.QTableWidgetItem(str(each_score[2])))
                    self.view_classes_score_table.setItem(row_counter, 3,
                                                          QtWidgets.QTableWidgetItem(str(each_score[3])))
                    self.view_classes_score_table.setItem(row_counter, 4,
                                                          QtWidgets.QTableWidgetItem(str(each_score[4])))
        else:
            self.view_classes_score_table.setColumnCount(4)
            self.view_classes_score_table.setHorizontalHeaderLabels(["Homework", "Score", "Percentage", "Attempts"])
            scores: list = ui_scripts.get_scores_of_student_in_class(current_class, current_student_or_homework)
            self.view_classes_score_table.setRowCount(len(scores))
            if len(scores) != 0:
                row_counter: int = -1
                for each_score in scores:
                    row_counter += 1
                    self.view_classes_score_table.setItem(row_counter, 0, QtWidgets.QTableWidgetItem(each_score[0]))
                    self.view_classes_score_table.setItem(row_counter, 1,
                                                          QtWidgets.QTableWidgetItem(str(each_score[1])))
                    self.view_classes_score_table.setItem(row_counter, 2,
                                                          QtWidgets.QTableWidgetItem(str(each_score[2])))
                    self.view_classes_score_table.setItem(row_counter, 3,
                                                          QtWidgets.QTableWidgetItem(str(each_score[3])))

    # </editor-fold>

    # <editor-fold desc="Homework Select Page">
    def homework_select_reset_page(self):
        # Clears class selection combo box
        self.homework_select_class_combo_box.clear()
        # Inserts class list into combo box
        self.student_classes: list = ui_scripts.get_classes_of_student(self.current_user)
        for each_class in self.student_classes:
            self.homework_select_class_combo_box.addItem(each_class[1])
        # Updates score table to first class selected
        self.homework_select_update_table()

    def homework_select_page_button_setup(self):
        # When selected class is changed, score table is updated
        self.homework_select_class_combo_box.currentIndexChanged.connect(lambda: self.homework_select_update_table())
        # When table double clicked, runs scripts to go to selected homework
        self.homework_select_table.doubleClicked.connect(self.homework_select_table_clicked)

    def homework_select_update_table(self):
        self.homework_select_table.clearContents()
        if len(self.student_classes) != 0:
            homework_ids: list = []
            self.homework_select_valid_homework_ids: list = []
            for each_homework in ui_scripts.get_homework_of_class(
                    self.student_classes[self.homework_select_class_combo_box.currentIndex()][0]):
                homework_ids.append(each_homework[0])
            for each_homework in homework_ids:
                data: tuple = ui_scripts.get_homework_name_and_due_date(each_homework, self.student_classes[
                    self.homework_select_class_combo_box.currentIndex()][0])
                due_year_month_day: list = data[1].split('-')
                due_date: datetime.date = datetime.date(int(due_year_month_day[0]), int(due_year_month_day[1]),
                                                        int(due_year_month_day[2]))
                if datetime.date.today() < due_date:
                    self.homework_select_valid_homework_ids.append([each_homework, data[0], data[1]])
            self.homework_select_table.setRowCount(len(self.homework_select_valid_homework_ids))
            row_counter: int = -1
            for each_homework in self.homework_select_valid_homework_ids:
                row_counter += 1
                self.homework_select_table.setItem(row_counter, 0, QtWidgets.QTableWidgetItem(each_homework[1]))
                self.homework_select_table.setItem(row_counter, 1, QtWidgets.QTableWidgetItem(each_homework[2]))

    def homework_select_table_clicked(self):
        homework_id = self.homework_select_valid_homework_ids[self.homework_select_table.currentRow()][0]
        self.current_homework_questions: list = ui_scripts.get_questions_of_homework(homework_id)
        if len(self.current_homework_questions) > 0:
            self.change_page(self.question_page)
        else:
            return

    # </editor-fold>


# Runs program
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
