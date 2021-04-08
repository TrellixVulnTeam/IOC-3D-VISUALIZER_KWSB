import threading

import cv2
import mouse
from sound_manager import SoundManager


class VideoManager:
    def __init__(self, int_width, int_height, cam_width, cam_height):
        self.cam_width = cam_width
        self.cam_height = cam_height

        self.interface_width = int_width
        self.interface_height = int_height

        self.face_cascade = cv2.CascadeClassifier('venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

        self.close = False

    def calibrate(self, vid, direction):
        self.close = False
        calibrated_value = None

        for i in range(60):
            ret, frame = vid.read()
            frame = cv2.resize(frame, (self.cam_width, self.cam_height))
            if ret:
                cvImg = cv2.flip(frame, 1)
                gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
                faceRects = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                cv2.putText(cvImg, 'Calibrate ' + str(direction) + ': ' + str(int(i / 0.6)) + '%',
                            (int(self.cam_width / 2) - 150, int(self.cam_height / 2)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4, cv2.LINE_AA)
                if direction == 'Left':
                    cvImg = cv2.circle(cvImg, (0, int(self.cam_height / 2)), 50, (0, 255, 255), -1)
                elif direction == 'Right':
                    cvImg = cv2.circle(cvImg, (self.cam_width, int(self.cam_height / 2)), 50, (0, 255, 255), -1)
                elif direction == 'Up':
                    cvImg = cv2.circle(cvImg, (int(self.cam_width / 2), 0), 50, (0, 255, 255), -1)
                elif direction == 'Down':
                    cvImg = cv2.circle(cvImg, (int(self.cam_width / 2), self.cam_height), 50, (0, 255, 255), -1)

                for (x, y, w, h) in faceRects:
                    cvImg = cv2.rectangle(cvImg, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    if direction == 'Left':
                        calibrated_value = x + w / 2
                    elif direction == 'Right':
                        calibrated_value = x + w / 2
                    elif direction == 'Up':
                        calibrated_value = y + h / 2
                    elif direction == 'Down':
                        calibrated_value = y + h / 2

            cv2.imshow('frame', cvImg)
            if cv2.waitKey(1) & 0xFF == ord('\r'):
                break

        return calibrated_value

    def video_stream(self):
        sound_manager = SoundManager()
        vid = cv2.VideoCapture(0)

        xf_min = self.calibrate(vid, 'Left')
        thread = threading.Thread(target=sound_manager.play_calibrate_sound)
        thread.start()
        xf_max = self.calibrate(vid, 'Right')
        thread = threading.Thread(target=sound_manager.play_calibrate_sound)
        thread.start()
        yf_min = self.calibrate(vid, 'Up')
        thread = threading.Thread(target=sound_manager.play_calibrate_sound)
        thread.start()
        yf_max = self.calibrate(vid, 'Down')
        thread = threading.Thread(target=sound_manager.play_successfully_calibration_sound)
        thread.start()

        while not self.close:
            ret, frame = vid.read()
            frame = cv2.resize(frame, (self.cam_width, self.cam_height))
            if ret:
                cvImg = cv2.flip(frame, 1)
                gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
                faceRects = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faceRects:
                    cvImg = cv2.rectangle(cvImg, (x, y), (x + w, y + h), (255, 0, 0), 3)

                    xf = x + w / 2
                    yf = y + h / 2

                    if xf < xf_min:
                        xf = xf_min

                    if xf > xf_max:
                        xf = xf_max

                    if yf < yf_min:
                        yf = yf_min

                    if yf > yf_max:
                        yf = yf_max

                    xp_min = 0
                    xp_max = self.interface_width
                    yp_min = 0
                    yp_max = self.interface_height

                    xp = xf * ((xp_max - xp_min) / (xf_max - xf_min)) + xp_min - (
                            (xp_max - xp_min) / (xf_max - xf_min)) * xf_min
                    yp = yf * ((yp_max - yp_min) / (yf_max - yf_min)) + yp_min - (
                            (yp_max - yp_min) / (yf_max - yf_min)) * yf_min

                    xp = int(xp)
                    yp = int(yp)
                    xp = xp - xp % 50
                    yp = yp - yp % 50

                    if xp > self.interface_width:
                        xp = self.interface_width

                    if yp > self.interface_height:
                        yp = self.interface_height

                    cv2.imshow('frame', cvImg)
                    mouse.move(xp / xp_max * 1920, yp / yp_max * 1080, absolute=True, duration=0)

            if cv2.waitKey(1) & 0xFF == ord('r'):
                break

        vid.release()
