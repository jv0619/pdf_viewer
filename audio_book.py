import pyttsx3
from threading import Thread


class Speak(Thread):
    def __init__(self, text, **kw):
        super().__init__(**kw)
        # Initializing the Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('rate', 200)

        # Initializing read words
        self.sentences = text.split('\n')
        self.paused = False
        self.running = False

    def run(self):
        self.running = True
        while self.sentences and self.running:
            if not self.paused:
                sentence = self.sentences.pop(0)
                self.engine.say(sentence)
                self.engine.runAndWait()
        self.running = False

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False



