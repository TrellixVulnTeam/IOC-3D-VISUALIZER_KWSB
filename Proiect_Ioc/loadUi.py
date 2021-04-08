import threading

import cv2
import win32gui
from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog

from color_manager import ColorManager
from sound_manager import SoundManager
from video_manager import VideoManager
from scene_manager import SceneManager
from process_communication_manager import ProcessCommunicationManager
from audio_manager import AudioManager


class Ui(QtWidgets.QMainWindow):
    def __init__(self, style):
        super(Ui, self).__init__()
        uic.loadUi('qt_interface.ui', self)

        self.color_manager = ColorManager(style)
        self.sound_manager = SoundManager()
        self.camera_manager = VideoManager(self.width(), self.height(), self.cameraWidget.width(),
                                           self.cameraWidget.height())

        self.camera_thread = None
        self.buttons = self.getAllButtons()
        self.checkboxes = [self.videoControlCheckBox, self.voiceControlCheckBox, self.darkControlCheckBox]
        self.initializeColors()

        self.loadButton.clicked.connect(self.on_load_button_clicked)
        self.rotateLeftButton.clicked.connect(self.on_rotate_left_button_clicked)
        self.rotateRightButton.clicked.connect(self.on_rotate_right_button_clicked)
        self.rotateUpButton.clicked.connect(self.on_rotate_up_button_clicked)
        self.rotateDownButton.clicked.connect(self.on_rotate_down_button_clicked)
        self.zoomInButton.clicked.connect(self.on_zoom_in_button_clicked)
        self.zoomOutButton.clicked.connect(self.on_zoom_out_button_clicked)
        self.videoControlCheckBox.toggled.connect(self.on_video_control_checkbox_checked)
        self.voiceControlCheckBox.toggled.connect(self.on_voice_control_checkbox_checked)
        self.darkControlCheckBox.toggled.connect(self.on_dark_theme_control_checkbox_checked)

        self.scene = None
        self.processCommunicationManager = ProcessCommunicationManager()
        self.show()

        self.audio_manager = AudioManager(self)
        self.initAudioListener()


    def initAudioListener(self):
        self.audio_manager.start()

    def getAllButtons(self):
        buttons = [self.loadButton, self.rotateLeftButton, self.rotateRightButton, self.rotateUpButton,
                   self.rotateDownButton, self.zoomInButton, self.zoomOutButton]

        return buttons

    def initializeColors(self):
        self.color_manager.set_colors(self, self.buttons, self.checkboxes, self.cameraWidget, self.sceneWidget)

    def closeEvent(self, event):
        self.processCommunicationManager.close()

    def on_load_button_clicked(self):
        self.sound_manager.play_button_click_sound()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, "3d object picker", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        if path:
            print(path)
            self.initScene()
            self.processCommunicationManager.send_message("file " + path)

    def on_rotate_left_button_clicked(self):
        self.sound_manager.play_button_click_sound()
        self.processCommunicationManager.send_message("left")

    def on_rotate_right_button_clicked(self):
        self.sound_manager.play_button_click_sound()
        self.processCommunicationManager.send_message("right")

    def on_rotate_up_button_clicked(self):
        self.sound_manager.play_button_click_sound()
        self.processCommunicationManager.send_message("up")

    def on_rotate_down_button_clicked(self):
        self.sound_manager.play_button_click_sound()
        self.processCommunicationManager.send_message("down")

    def on_zoom_in_button_clicked(self):
        self.sound_manager.play_button_click_sound()
        self.processCommunicationManager.send_message("zoomIn")

    def on_zoom_out_button_clicked(self):
        self.sound_manager.play_button_click_sound()
        self.processCommunicationManager.send_message("zoomOut")

    def on_dark_theme_control_checkbox_checked(self):
        self.sound_manager.play_button_click_sound()
        if self.darkControlCheckBox.checkState() == 2:
            self.color_manager = ColorManager("dark")
            self.initializeColors()
        else:
            self.color_manager = ColorManager("light")
            self.initializeColors()

    def on_video_control_checkbox_checked(self):
        self.sound_manager.play_button_click_sound()
        if self.videoControlCheckBox.checkState() == 2:
            self.initCamera()
        else:
            self.destroyCamera()

    def on_voice_control_checkbox_checked(self):
        self.sound_manager.play_button_click_sound()

    def initCamera(self):
        self.camera_manager.close = False
        img = cv2.imread('resources/images/loading.png')
        img = cv2.resize(img, (self.cameraWidget.width(), self.cameraWidget.height()))
        cv2.imshow('frame', img)

        self.camera_thread = threading.Thread(target=self.camera_manager.video_stream)
        self.camera_thread.start()

        camera_layout = QVBoxLayout(self.cameraWidget)
        hwnd = win32gui.FindWindow(None, "frame")
        cam_window = QWindow.fromWinId(hwnd)
        camera_widget = QWidget.createWindowContainer(cam_window)
        camera_widget.setGeometry(self.cameraWidget.x(), self.cameraWidget.x(), self.cameraWidget.width(),
                                  self.cameraWidget.height())
        camera_layout.addWidget(camera_widget)

    def destroyCamera(self):
        self.camera_manager.close = True
        self.camera_thread.join()
        img = cv2.imread('resources/images/turnedoff.png')
        img = cv2.resize(img, (self.cameraWidget.width(), self.cameraWidget.height()))
        cv2.imshow('frame', img)

    def initScene(self):
        layout = QVBoxLayout(self.sceneWidget)
        hwnd = win32gui.FindWindow(None, "scene")
        scene_window = QWindow.fromWinId(hwnd)
        widget = QWidget.createWindowContainer(scene_window)
        widget.setGeometry(0, 0, self.sceneWidget.width(),
                           self.sceneWidget.height())
        layout.addWidget(widget)

    def createScene(self):
        self.scene = SceneManager(self.sceneWidget.width() - 50, self.sceneWidget.height() - 50)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui("light")
    app.exec_()
