from PyQt5 import QtWidgets
from PyQt5 import uic

# 'pyrcc5 -o window_rc.py window.qrc' Used to generate resource file (window_rc.py)
from scripts import login_scripts


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
        # Set start page to login screen
        self.change_page(self.login_page)
        self.button_setup()
        self.reset_pages()
        # Disables logout button until logged in
        self.hide_logout_button()
        # Holds ID of active user
        self.current_user = 1

    def logout(self):
        # Resets current user to a default value
        self.current_user = 1
        # Returns to login page
        self.change_page(self.login_page)
        # Hides login button
        self.hide_logout_button()

    def go_to_main_menu(self):
        if login_scripts.get_account_type(self.current_user) == 't':
            self.change_page(self.teacher_main_menu_page)
        else:
            self.change_page(self.student_main_menu_page)

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
        self.student_main_menu_browse_quizzes_button.clicked.connect(lambda: self.change_page(self.browse_quizzes_page))
        self.student_main_menu_homework_button.clicked.connect(lambda: self.change_page(self.homework_select_page))
        self.student_main_menu_previous_scores_button.clicked.connect(
            lambda: self.change_page(self.previous_scores_page))

    def teacher_main_menu_page_button_setup(self):
        self.teacher_main_menu_set_homework_button.clicked.connect(lambda: self.change_page(self.set_homework_page))
        self.teacher_main_menu_view_classes_button.clicked.connect(lambda: self.change_page(self.view_classes_page))

    def button_setup(self):
        # If logout button clicked runs logout scripts
        self.logout_button.clicked.connect(self.logout)
        self.main_menu_button.clicked.connect(self.go_to_main_menu)
        self.login_page_button_setup()
        self.create_account_page_button_setup()
        self.student_main_menu_page_button_setup()
        self.teacher_main_menu_page_button_setup()

    def reset_pages(self):
        # Sets radios to default selection
        self.create_account_radio_student.setChecked(True)
        self.question_radio_a.setChecked(True)
        # Sets input boxes to blank
        self.login_username_input.setText("")
        self.login_password_input.setText("")
        self.create_account_first_name_input.setText("")
        self.create_account_last_name_input.setText("")
        self.create_account_username_input.setText("")
        self.create_account_password_input.setText("")
        self.create_account_password_verify_input.setText("")
        self.question_topic_output.setText("")
        self.question_question_output.setText("")
        self.question_radio_a.setText("")
        self.question_radio_b.setText("")
        self.question_radio_c.setText("")
        self.question_radio_d.setText("")
        # Sets output labels to blank
        self.login_success_output.setText("")
        self.create_account_success_output.setText("")
        self.question_feedback_output.setText("")

    def hide_logout_button(self):
        # Disables and hides the logout button
        self.logout_button.setEnabled(False)
        self.logout_button.setVisible(False)
        # Disables amd hides main menu button
        self.main_menu_button.setEnabled(False)
        self.main_menu_button.setVisible(False)
        # Stops showing the user's first name
        self.username_label.setText("")

    def show_logout_button(self):
        # Enables and shows logout button
        self.logout_button.setEnabled(True)
        self.logout_button.setVisible(True)
        # Enables and shows main menu button
        self.main_menu_button.setEnabled(True)
        self.main_menu_button.setVisible(True)
        # Makes the user's first name show in the top left corner
        self.username_label.setText(login_scripts.get_first_name(self.current_user).title())

    def login(self):
        # Checks if username exists (case fold used to make username case insensitive even for characters such as ß)
        if login_scripts.check_user_exists(self.login_username_input.text().casefold()):
            # Checks if password is correct. If password correct next screen loaded
            user_id = login_scripts.get_user_id(self.login_username_input.text().casefold())
            if login_scripts.check_password(user_id, self.login_password_input.text()):
                self.login_success_output.setText("Success")
                self.current_user = user_id
                self.show_logout_button()
                if login_scripts.get_account_type(self.current_user) == 't':
                    self.change_page(self.teacher_main_menu_page)
                elif login_scripts.get_account_type(self.current_user) == 's':
                    self.change_page(self.student_main_menu_page)
            # If password incorrect, invalid password error is displayed and password box is cleared
            else:
                self.login_success_output.setText("Invalid password")
                self.login_password_input.setText("")
        # If username did not exist, invalid username error is displayed
        else:
            self.login_success_output.setText("Invalid username")

    def change_page(self, index: int):
        # Changes the current page index to the value passed
        self.reset_pages()
        self.main_widget.setCurrentIndex(index)

    def get_account_type_selected(self) -> str:
        # Returns whether student or teacher is selected (or neither, though this should never occur)
        if self.create_account_radio_student.isChecked():
            return 's'
        elif self.create_account_radio_teacher.isChecked():
            return 't'
        else:
            return ''

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
            self.reset_pages()
            # Account creation success outputted
            self.create_account_success_output.setText("Account created")


# If run as main launch into test conditions
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
