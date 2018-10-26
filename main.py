import sys

from PyQt5 import QtWidgets

import window as login_ui


# Generic code to start the program UI
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = login_ui.Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
