import threading

import cv2
import win32gui
from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from color_manager import ColorManager
from sound_manager import SoundManager
from video_manager import VideoTracking


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('qt_interface.ui', self)

        self.color_manager = ColorManager()
        self.sound_manager = SoundManager()
        self.camera_manager = VideoTracking(self.width(), self.height(), self.cameraWidget.width(),
                                            self.cameraWidget.height())

        self.buttons = self.getAllButtons()
        self.checkboxes = [self.videoControlCheckBox, self.voiceControlCheckBox]
        self.initializeColors()

        self.loadButton.clicked.connect(self.on_load_button_clicked)
        self.exitButton.clicked.connect(self.on_exit_button_clicked)
        self.rotateLeftButton.clicked.connect(self.on_rotate_left_button_clicked)
        self.rotateRightButton.clicked.connect(self.on_rotate_right_button_clicked)
        self.rotateUpButton.clicked.connect(self.on_rotate_up_button_clicked)
        self.rotateDownButton.clicked.connect(self.on_rotate_down_button_clicked)
        self.zoomInButton.clicked.connect(self.on_zoom_in_button_clicked)
        self.zoomOutButton.clicked.connect(self.on_zoom_out_button_clicked)
        self.videoControlCheckBox.toggled.connect(self.on_video_control_checkbox_checked)
        self.voiceControlCheckBox.toggled.connect(self.on_voice_control_checkbox_checked)

        self.show()

    def getAllButtons(self):
        buttons = [self.loadButton, self.exitButton, self.rotateLeftButton, self.rotateRightButton, self.rotateUpButton,
                   self.rotateDownButton, self.zoomInButton, self.zoomOutButton]

        return buttons

    def initializeColors(self):
        self.color_manager.set_colors(self, self.buttons, self.checkboxes, self.cameraWidget, self.objectSceneWidget)

    def on_load_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_exit_button_clicked(self):
        self.sound_manager.play_quit_sound()

    def on_rotate_left_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_rotate_right_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_rotate_up_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_rotate_down_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_zoom_in_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_zoom_out_button_clicked(self):
        self.sound_manager.play_button_click_sound()

    def on_video_control_checkbox_checked(self):

        self.sound_manager.play_button_click_sound()
        if self.videoControlCheckBox.checkState() == 2:
            self.initCamera()
        else:
            self.destroyCamera()

    def on_voice_control_checkbox_checked(self):
        self.sound_manager.play_button_click_sound()

    def initCamera(self):
        img = cv2.imread('loading.png')
        img = cv2.resize(img, (self.cameraWidget.width(), self.cameraWidget.height()))
        cv2.imshow('frame', img)

        camera_thread = threading.Thread(target=self.camera_manager.video_stream)
        camera_thread.start()

        layout = QVBoxLayout(self.cameraWidget)
        hwnd = win32gui.FindWindow(None, "frame")
        cam_window = QWindow.fromWinId(hwnd)
        widget = QWidget.createWindowContainer(cam_window)
        widget.setGeometry(self.cameraWidget.x(), self.cameraWidget.x(), 1000, 1000)
        layout.addWidget(widget)

    def destroyCamera(self):
        self.camera_manager.close = True


pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
