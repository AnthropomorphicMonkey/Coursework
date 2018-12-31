from PyQt5 import QtWidgets
from PyQt5 import uic

# 'pyrcc5 -o window_rc.py window.qrc' Used to generate resource file (window_rc.py)
from scripts import login_scripts, ui_scripts


# Window class to control uid
class Window(QtWidgets.QMainWindow, uic.loadUiType('window.ui')[0]):
    # noinspection PyArgumentList
    def __init__(self):
        # Inherits from generic window class from QT
        super().__init__()
        self.setupUi(self)
        # Declare constants related to page indexes of different sections of the program
        self.login_page = 0
        self.create_account_page = 1
        self.student_main_menu_page = 2
        self.teacher_main_menu_page = 3
        self.question_page = 4
        self.homework_select_page = 5
        self.browse_quizzes_page = 6
        self.previous_scores_page = 7
        self.set_homework_page = 8
        self.admin_page = 9
        self.account_management_page = 10
        self.view_classes_page = 11
        # Holds ID of active user
        self.current_user = -1
        # Clears list of user classes
        self.user_classes = []
        self.teacher_classes = []
        self.class_users = []
        # Sets up all pages
        self.button_setup()
        self.reset_pages(self.login_page)
        # Sets program to logged out state (and hides logged out message)
        self.logout()
        self.login_success_output.setText("")

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

    def get_account_type_selected(self) -> str:
        # Returns whether student or teacher is selected (or neither, though this should never occur)
        if self.create_account_radio_student.isChecked():
            return 's'
        elif self.create_account_radio_teacher.isChecked():
            return 't'
        else:
            return ''

    def login(self):
        # Checks if username exists (case fold used to make username case insensitive even for characters such as ß)
        if login_scripts.check_user_exists(self.login_username_input.text().casefold()):
            # Checks if password is correct
            user_id = login_scripts.get_user_id(self.login_username_input.text().casefold())
            if login_scripts.check_password(user_id, self.login_password_input.text()):
                # Checks user type to decide which main menu to load
                if login_scripts.get_account_type(user_id) in ['s', 't']:
                    self.login_success_output.setText("Success")
                    self.current_user = user_id
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

    def logout(self):
        # Resets current user to a default value
        self.current_user = -1
        # Returns to login page and sets logout success message
        self.change_page(self.login_page)
        self.login_success_output.setText("Logout successful")

    def hide_main_menu_button(self):
        # Disables amd hides main menu button
        self.main_menu_button.setEnabled(False)
        self.main_menu_button.setVisible(False)

    def show_main_menu_button(self):
        # Enables and shows main menu button
        self.main_menu_button.setEnabled(True)
        self.main_menu_button.setVisible(True)

    def show_username_text(self):
        # Makes the user's first name show in ui
        self.username_label.setText(login_scripts.get_first_name(self.current_user).title())

    def hide_username_text(self):
        # Stops showing the user's first name in ui
        self.username_label.setText("")

    def hide_logout_button(self):
        # Disables and hides the logout button
        self.logout_button.setEnabled(False)
        self.logout_button.setVisible(False)

    def show_logout_button(self):
        # Enables and shows logout button
        self.logout_button.setEnabled(True)
        self.logout_button.setVisible(True)

    def go_to_main_menu(self):
        # Returns to the correct main menu page for the given user
        if login_scripts.get_account_type(self.current_user) == 't':
            self.change_page(self.teacher_main_menu_page)
        elif login_scripts.get_account_type(self.current_user) == 's':
            self.change_page(self.student_main_menu_page)
        # If data in DB is for some reason invalid, user is logged out and error shown
        else:
            self.logout()
            self.login_success_output.setText("User type error, user has been logged out")

    def navigation_button_setup(self):
        # If logout button clicked runs logout scripts
        self.logout_button.clicked.connect(self.logout)
        self.main_menu_button.clicked.connect(self.go_to_main_menu)

    def login_page_button_setup(self):
        # If login submit button clicked runs scripts to verify login
        self.login_submit_button.clicked.connect(self.login)
        # If create account clicked runs scripts to change screen
        # Error passing arguments fixed using https://stackoverflow.com/questions/45793966/clicked-connect-error
        self.login_create_account_button.clicked.connect(lambda: self.change_page(self.create_account_page))

    def create_account_page_button_setup(self):
        # If create account submit button clicked runs scripts to create account
        self.create_account_submit_button.clicked.connect(self.create_account)
        # If return to login clicked runs scripts to change screen
        self.create_account_login_button.clicked.connect(lambda: self.change_page(self.login_page))

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

    def previous_scores_page_button_setup(self):
        # When selected class is changed, score table is updated
        self.previous_scores_class_combo_box.currentIndexChanged.connect(lambda: self.update_previous_scores_table())

    def admin_page_button_setup(self):
        self.admin_class_user_combo_box.currentIndexChanged.connect(lambda: self.update_admin_username_combo_box())
        self.admin_username_submit_button.clicked.connect(lambda: self.add_user_to_class())
        self.admin_create_class_submit_button.clicked.connect(lambda: self.admin_create_class())
        self.admin_remove_user_button.clicked.connect(lambda: self.remove_user_from_class())
        self.admin_remove_class_button.clicked.connect(lambda: self.remove_class())

    def button_setup(self):
        # Runs all button setups
        self.navigation_button_setup()
        self.login_page_button_setup()
        self.create_account_page_button_setup()
        self.student_main_menu_page_button_setup()
        self.teacher_main_menu_page_button_setup()
        self.previous_scores_page_button_setup()
        self.admin_page_button_setup()

    def reset_login_page(self):
        # Sets input boxes to blank
        self.login_username_input.setText("")
        self.login_password_input.setText("")
        # Sets output labels to blank
        self.login_success_output.setText("")

    def reset_create_account_page(self):
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

    def reset_question_page(self):
        self.question_radio_a.setChecked(True)
        # Sets input boxes to blank
        self.question_topic_output.setText("")
        self.question_question_output.setText("")
        self.question_radio_a.setText("")
        self.question_radio_b.setText("")
        self.question_radio_c.setText("")
        self.question_radio_d.setText("")
        # Sets output labels to blank
        self.question_feedback_output.setText("")

    def reset_previous_scores_page(self):
        # Clears class selection combo box
        self.previous_scores_class_combo_box.clear()
        # Inserts class list into combo box
        self.user_classes = ui_scripts.get_classes_of_user(self.current_user)
        for each_class in self.user_classes:
            self.previous_scores_class_combo_box.addItem(each_class[1])
        # Updates score table to first class selected
        self.update_previous_scores_table()

    def reset_admin_page(self):
        self.admin_class_user_combo_box.clear()
        self.admin_delete_class_combo_box.clear()
        self.teacher_classes = ui_scripts.get_classes_of_teacher(self.current_user)
        for each_class in self.teacher_classes:
            self.admin_class_user_combo_box.addItem(each_class[1])
            self.admin_delete_class_combo_box.addItem(each_class[1])
        self.update_admin_username_combo_box()
        self.admin_username_input.setText("")
        self.admin_class_input.setText("")
        self.admin_add_user_status_label.setText("")
        self.admin_remove_user_status_label.setText("")
        self.admin_create_class_status_label.setText("")
        self.admin_delete_class_status_label.setText("")

    def reset_pages(self, target_page):
        # Runs all page reset scripts
        if target_page == self.login_page:
            self.reset_login_page()
        elif target_page == self.create_account_page:
            self.reset_create_account_page()
        elif target_page == self.question_page:
            self.reset_question_page()
        elif target_page == self.previous_scores_page:
            self.reset_previous_scores_page()
        elif target_page == self.admin_page:
            self.reset_admin_page()
        else:
            pass

    def create_account(self):
        # Various error checks before creating account (error type is outputted in a label):
        # Error if username field is blank
        if self.create_account_username_input.text() == '':
            self.create_account_success_output.setText("Invalid username")
        # Error if username already taken
        elif login_scripts.check_user_exists(self.create_account_username_input.text().casefold()):
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
            login_scripts.create_account(self.create_account_username_input.text().casefold(),
                                         self.create_account_password_input.text(),
                                         self.create_account_first_name_input.text(),
                                         self.create_account_last_name_input.text(),
                                         self.get_account_type_selected())
            # Resets create account page once account successfully created
            self.reset_pages(self.create_account_page)
            # Account creation success outputted
            self.create_account_success_output.setText("Account created")

    def update_previous_scores_table(self):
        self.previous_scores_table.clearContents()
        if len(self.user_classes) != 0:
            homework_ids = []
            for each_homework in ui_scripts.get_homeworks_of_class(
                    self.user_classes[self.previous_scores_class_combo_box.currentIndex()][0]):
                homework_ids.append(each_homework[0])
            self.previous_scores_table.setRowCount(len(homework_ids))
            row_counter = -1
            for each_homework in homework_ids:
                row_counter += 1
                data = ui_scripts.get_homework_score(self.current_user, each_homework)
                self.previous_scores_table.setItem(row_counter, 0, QtWidgets.QTableWidgetItem(data[0]))
                self.previous_scores_table.setItem(row_counter, 1, QtWidgets.QTableWidgetItem("{}%".format(data[1])))
                self.previous_scores_table.setItem(row_counter, 2, QtWidgets.QTableWidgetItem(data[2]))

    def update_admin_username_combo_box(self):
        self.admin_username_combo_box.clear()
        if len(self.teacher_classes) != 0:
            self.class_users = ui_scripts.get_users_of_class(
                self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0])
            for each_user in self.class_users:
                self.admin_username_combo_box.addItem(each_user[1])

    def add_user_to_class(self):
        user = self.admin_username_input.text()
        # Stops scripts being able to run if the teacher has no classes to add a student to
        if len(self.teacher_classes) > 0:
            if login_scripts.check_user_exists(user):
                user_id = login_scripts.get_user_id(user)
                class_id = self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0]
                if ui_scripts.check_user_in_class(user_id, class_id):
                    self.admin_add_user_status_label.setText("User already in class")
                else:
                    ui_scripts.add_user_to_class(user_id, class_id)
                    self.reset_admin_page()
                    self.admin_add_user_status_label.setText("Success")
            else:
                self.admin_add_user_status_label.setText("User does not exist")
        self.admin_username_input.setText("")

    def remove_user_from_class(self):
        # Stops scripts being able to run if a student and/or class is not selected
        if len(self.class_users) > 0 and len(self.teacher_classes) > 0:
            user_id = self.class_users[self.admin_username_combo_box.currentIndex()][0]
            class_id = self.teacher_classes[self.admin_class_user_combo_box.currentIndex()][0]
            ui_scripts.remove_user_from_class(user_id, class_id)
            self.reset_admin_page()
            self.admin_remove_user_status_label.setText("Success")
        else:
            self.admin_remove_user_status_label.setText("")

    def admin_create_class(self):
        pass

    def remove_class(self):
        pass


# Runs program
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
