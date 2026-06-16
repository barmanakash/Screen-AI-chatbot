import os
import speech_recognition as sr
import pyaudiowpatch as pyaudio
sr.pyaudio = pyaudio

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_and_transcribe(self) -> str:
        """Listens from the default local microphone and transcribes it."""
        print("[Voice Engine]: Listening...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
        try:
            # Uses free, localized web engine processing fallback
            text = self.recognizer.recognize_google(audio)
            print(f"[Voice Engine Input Received]: {text}")
            return text.strip()
        except Exception:
            return ""

    def speak(self, text: str):
        """Uses native Windows speech synthesis engine (SAPI5) offline."""
        print(f"[Agent Audio Output]: {text}")
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except Exception:
            # System printing fallback if COM wrappers fail to trigger
            pass