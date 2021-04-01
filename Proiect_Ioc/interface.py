import subprocess
import sys
import time

import win32gui
import win32process
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)

    hwnd = win32gui.FindWindow(None,"Aruco 3D App")
    window = QWindow.fromWinId(hwnd)


    widget = QWidget.createWindowContainer(window)
    widget.setGeometry(500, 500, 450, 400)
    widget.setWindowTitle('File dialog')

    layout.addWidget(widget)

    button = QPushButton('Close')
    button.clicked.connect(main_widget.close)
    layout.addWidget(button)

    main_widget.show()
    app.exec_()





