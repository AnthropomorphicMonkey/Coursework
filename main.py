import sys

from PyQt5 import QtWidgets

import login_ui as login_ui


# Generic code to start the program UI
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = login_ui.LoginWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
