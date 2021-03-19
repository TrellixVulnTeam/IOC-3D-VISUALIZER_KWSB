import imutils as imutils
import cv2
import threading

cam_width = 800
cam_height = 600

interface_width = 1000
interface_height = 750

face_cascade = cv2.CascadeClassifier('venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')


def calibrate(vid, direction):
    calibrated_value = None
    #medie -> pentru zogmot
    for i in range(300):
        ret, frame = vid.read()
        frame = imutils.resize(frame, width=cam_width, height=cam_height)
        if ret:
            cvImg = cv2.flip(frame, 1)
            gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
            faceRects = face_cascade.detectMultiScale(gray, 1.3, 5)

            cv2.putText(cvImg, 'Calibrate ' + str(direction) + ': ' + str(int(i / 3)) + '%',
                        (int(cam_width / 2) - 150, int(cam_height / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4, cv2.LINE_AA)
            if direction == 'Left':
                cvImg = cv2.circle(cvImg, (0, int(cam_height / 2)), 50, (0, 255, 255), -1)
            elif direction == 'Right':
                cvImg = cv2.circle(cvImg, (cam_width, int(cam_height / 2)), 50, (0, 255, 255), -1)
            elif direction == 'Up':
                cvImg = cv2.circle(cvImg, (int(cam_width / 2), 0), 50, (0, 255, 255), -1)
            elif direction == 'Down':
                cvImg = cv2.circle(cvImg, (int(cam_width / 2), cam_height), 50, (0, 255, 255), -1)

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


def video_stream():
    vid = cv2.VideoCapture(0)
    xf_min = calibrate(vid, 'Left')
    xf_max = calibrate(vid, 'Right')
    yf_min = calibrate(vid, 'Up')
    yf_max = calibrate(vid, 'Down')

    while True:
        ret, frame = vid.read()
        frame = imutils.resize(frame, width=cam_width, height=cam_height)
        if ret:
            cvImg = cv2.flip(frame, 1)
            gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
            faceRects = face_cascade.detectMultiScale(gray, 1.3, 5)

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
                xp_max = interface_width
                yp_min = 0
                yp_max = interface_height

                xp = xf * ((xp_max - xp_min) / (xf_max - xf_min)) + xp_min - (
                        (xp_max - xp_min) / (xf_max - xf_min)) * xf_min
                yp = yf * ((yp_max - yp_min) / (yf_max - yf_min)) + yp_min - (
                        (yp_max - yp_min) / (yf_max - yf_min)) * yf_min

                xp = int(xp)
                yp = int(yp)
                xp = xp - xp % 50
                yp = yp - yp % 50

                if xp > interface_width:
                    xp = interface_width

                if yp > interface_height:
                    yp = interface_height

                cvImg = cv2.circle(cvImg, (xp, yp), 25, (0, 0, 255), -1)

        cv2.imshow('frame', cvImg)

        if cv2.waitKey(1) & 0xFF == ord('r'):
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    x = threading.Thread(target=video_stream)
    x.start()
