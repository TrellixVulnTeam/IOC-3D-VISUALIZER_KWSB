import json


class ColorManager:
    def __init__(self):
        f = open("resources/styles/style.json", 'r')
        self.data = json.load(f)

    def set_colors(self, main_window, buttons, check_buttons, camera_widget, object_scene_widget):
        for b in buttons:
            b.setStyleSheet(
                'QPushButton {{background-color: {}; color: {} }};'.format(self.data["buttonBackgroundColor"],
                                                                           self.data[
                                                                               "buttonTextColor"],
                                                                           ))
        for b in check_buttons:
            b.setStyleSheet('QCheckBox {{color: {}}};'.format(self.data["buttonTextColor"]))

        camera_widget.setStyleSheet('QWidget {{background-color: {}}};'.format(self.data["cameraPlaceholderColor"]))
        object_scene_widget.setStyleSheet(
            'QWidget {{background-color: {}}};'.format(self.data["scenePlaceholderColor"]))
        main_window.setStyleSheet('QMainWindow {{background-color: {}}};'.format(self.data["backgroundColor"]))
