import threading

import playsound as sound_player


class SoundManager:
    def __init__(self):
        self.path = "resources/sounds"

    def play_wait_sound(self):
        thread = threading.Thread(target=sound_player.playsound, args=[self.path + '/loading.wav'])
        thread.start()

    def play_button_click_sound(self):
        thread = threading.Thread(target=sound_player.playsound, args=[self.path + '/button_clicked.wav'])
        thread.start()

    def play_calibrate_sound(self):
        thread = threading.Thread(target=sound_player.playsound, args=[self.path + '/calibration.wav'])
        thread.start()

    def play_successfully_calibration_sound(self):
        thread = threading.Thread(target=sound_player.playsound, args=[self.path + '/successfully_calibration.wav'])
        thread.start()

    def play_quit_sound(self):
        thread = threading.Thread(target=sound_player.playsound, args=[self.path + '/quit.wav'])
        thread.start()