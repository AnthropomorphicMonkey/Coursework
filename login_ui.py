from PyQt5 import QtWidgets
from PyQt5 import uic

import login_scripts


# Window class to control uid
class LoginWindow(QtWidgets.QMainWindow, uic.loadUiType('login.ui')[0]):
    def __init__(self):
        # Inherits from generic window class from QT
        super().__init__()
        self.setupUi(self)
        # Declare constants related to page indexes of different sections of the program
        self.login_page = 0
        self.create_account_page = 1
        # Set start page to login screen
        self.change_page(self.login_page)
        # If login submit button clicked runs scripts to verify login
        self.login_submit_button.clicked.connect(self.login)
        # If create account submit button clicked runs scripts to create account
        self.create_account_submit_button.clicked.connect(self.create_account)
        # If create account clicked runs scripts to change screen
        # Error passing arguments fixed using https://stackoverflow.com/questions/45793966/clicked-connect-error
        self.login_create_account_button.clicked.connect(lambda: self.change_page(self.create_account_page))
        # If return to login clicked runs scripts to change screen
        self.create_account_login_button.clicked.connect(lambda: self.change_page(self.login_page))
        # Sets the default selected account type as student
        self.create_account_radio_student.setChecked(True)

    def login(self):
        # Checks if username exists (case fold used to make username case insensitive even for characters such as ß)
        if login_scripts.check_user_exists(self.login_username_input.text().casefold()):
            # Checks if password is correct
            # If password correct next screen loaded
            if login_scripts.check_password(self.login_username_input.text().casefold(),
                                            self.login_password_input.text()):
                self.login_success_output.setText("Success")
            # If password incorrect, invalid password error is displayed and password box is cleared
            else:
                self.login_success_output.setText("Invalid password")
                self.login_password_input.setText("")
        # If username did not exist, invalid username error is displayed
        else:
            self.login_success_output.setText("Invalid username")

    def change_page(self, index):
        # Changes the current page index to the value passed
        self.main_widget.setCurrentIndex(index)

    def get_account_type_selected(self):
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
        elif self.create_account_first_name_input.text() == '':
            self.create_account_success_output.setText("Invalid first name")
        # Error if no last name is entered
        elif self.create_account_last_name_input.text() == '':
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
            self.clear_create_account_page()
            # Account creation success outputted
            self.create_account_success_output.setText("Account created")

    def clear_create_account_page(self):
        # Resets all user inputs to default values
        self.create_account_first_name_input.setText("")
        self.create_account_last_name_input.setText("")
        self.create_account_username_input.setText("")
        self.create_account_password_input.setText("")
        self.create_account_password_verify_input.setText("")
        self.create_account_success_output.setText("")
        self.create_account_radio_student.setChecked(True)


# If run as main launch into test conditions
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
