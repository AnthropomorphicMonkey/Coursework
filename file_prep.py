import os

os.popen('pyuic5 window.ui -o window.py')
os.popen('pyrcc5 window.qrc -o window_rc.py')
