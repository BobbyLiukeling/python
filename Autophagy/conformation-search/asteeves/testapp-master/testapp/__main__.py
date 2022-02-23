from __future__ import (print_function, absolute_import, division,
                     unicode_literals)
import sys
import argparse

# import testapp
from PyQt5.QtWidgets import QApplication
from Classes import mGUI

def main():
    if not len(sys.argv) > 1:
        launch_gui()
    else:
        parser = argparse.ArgumentParser(description='This app is just a test')
        parser.add_argument('--gui', dest='gui', action='store_true',
                        help='Launch a PyQt gui rather than the command line')
        parser.add_argument('--no-gui', dest='gui',
                        action='store_false')
        args = parser.parse_args()
        print(args)

    if args.gui:
        launch_gui()

def launch_gui():
    print('The GUI is launching')
    app = QApplication(sys.argv)
    qw = mGUI.QuitWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
