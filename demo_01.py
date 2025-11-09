from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        IP = "169.254.174.210"  # adresa IP a lui NAO
        PORT = 9559

        tts = ALProxy("ALTextToSpeech", IP, PORT)
        video = ALProxy("ALVideoDevice", IP, PORT)

        nameId = video.subscribeCamera("camera_top", 0, 1, 13, 10)
        naoImage = video.getImageRemote(nameId)
        video.unsubscribe(nameId)

        if naoImage is None:
            tts.say("I haven't access to the camera.")
        else:
            tts.say("I have detected one person.")

        self.onStopped()  # terminarea box-ului

    def onInput_onStop(self):
        self.onStopped()