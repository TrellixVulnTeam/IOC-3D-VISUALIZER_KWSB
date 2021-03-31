import subprocess
import sys
import time

import win32gui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QWindow
from PyQt5.QtCore import pyqtSlot


def initUI(self):
    # create a process
    exePath = "C:\\Windows\\system32\\calc.exe"
    subprocess.Popen(exePath)

    hwnd = win32gui.FindWindowEx(0, 0, "CalcFrame", "计算器")
    time.sleep(0.05)
    window = QWindow.fromWinId(hwnd)

    self.createWindowContainer(window, self)
    self.setGeometry(500, 500, 450, 400)
    self.setWindowTitle('File dialog')
    self.show()

# def window():
#
#     widget = QWidget()
#
#     textLabel = QLabel(widget)
#     textLabel.setText("Hello World!")
#     textLabel.move(110, 85)
#
#     widget.setGeometry(50, 50, 320, 200)
#     widget.setWindowTitle("PyQt5 Example")
#     widget.show()
#     sys.exit(app.exec_())
#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    initUI(app)
