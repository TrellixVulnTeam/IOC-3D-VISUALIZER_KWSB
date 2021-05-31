import speech_recognition as sr
import pyttsx3
import threading


class AudioManager(threading.Thread):
    def __init__(self, interface):
        threading.Thread.__init__(self)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.quit = False
        self.buttons = []
        self.isInitialized = False
        self.interface = interface

    def speechToText(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.record(source, duration=5)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"

        return response

    def getQuitFlag(self):
        return self.quit

    def setQuitFlag(self):
        self.quit = True

    def textToSpeech(self, myText):
        self.engine.say(myText)
        self.engine.runAndWait()

    def set_buttons(self, buttons):
        self.buttons = buttons

    def state_1(self):
        action = 'Await Listening'
        print(action)
        self.state_2()

    def state_2(self):
        if not self.quit:
            text = self.speechToText()

            while not self.quit and (text["transcription"] is None or (
                    text["transcription"].lower() != "hello siri" and self.isInitialized == False)):
                text = self.speechToText()
                self.isInitialized = True

            print("Initialized")
            if not text["success"] and text["error"] == "API unavailable":
                print("ERROR: {}\n close program".format(text["error"]))
            else:
                self.state_3(text)
        else:
            print("Quit event triggered")

    def state_3(self, text):
        if not self.quit:
            if not text["success"]:
                print("I didn't catch that. What did you say?\n")
                self.state_2()
            else:
                self.state_4(text)
        else:
            print("Quit event triggered")

    def state_4(self, text):
        print(text["transcription"])

        if text["transcription"].lower() == 'up':
            self.interface.on_rotate_up_button_clicked()
        elif text["transcription"].lower() == 'down':
            self.interface.on_rotate_down_button_clicked()
        elif text["transcription"].lower() == 'left':
            self.interface.on_rotate_left_button_clicked()
        elif text["transcription"].lower() == 'right':
            self.interface.on_rotate_right_button_clicked()
        elif text["transcription"].lower() == 'zoom in':
            self.interface.on_zoom_in_button_clicked()
        elif text["transcription"].lower() == 'zoom out':
            self.interface.on_zoom_out_button_clicked()

        if not self.quit:
            self.state_1()
        else:
            print("Quit event triggered")


    def run(self):
        self.state_1()