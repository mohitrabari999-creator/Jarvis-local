"""Offline speech: pyttsx3 for talking, Vosk for listening (both optional)."""
from __future__ import annotations

import json
import queue
from pathlib import Path


class Speaker:
    def __init__(self, enabled: bool = True, rate: int = 180):
        self.engine = None
        if not enabled:
            return
        try:
            import pyttsx3

            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", rate)
        except Exception as e:  # missing driver, no audio device, etc.
            print(f"[voice] Text-to-speech disabled: {e}")

    def say(self, text: str) -> None:
        print(f"\n{text}\n")
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()


class Listener:
    """Offline speech recognition using a Vosk model folder."""

    def __init__(self, model_path: str):
        try:
            import sounddevice as sd
            from vosk import KaldiRecognizer, Model
        except ImportError as e:
            raise RuntimeError("Voice input needs: pip install vosk sounddevice") from e

        if not Path(model_path).exists():
            raise RuntimeError(
                f"Vosk model not found at '{model_path}'. Download one from "
                "https://alphacephei.com/vosk/models and unzip it there."
            )
        self.sd = sd
        self.samplerate = 16000
        self.recognizer = KaldiRecognizer(Model(model_path), self.samplerate)

    def listen(self) -> str:
        q: queue.Queue[bytes] = queue.Queue()

        def callback(indata, frames, time, status):
            q.put(bytes(indata))

        print("[listening...]")
        with self.sd.RawInputStream(
            samplerate=self.samplerate, blocksize=8000, dtype="int16", channels=1, callback=callback
        ):
            while True:
                if self.recognizer.AcceptWaveform(q.get()):
                    text = json.loads(self.recognizer.Result()).get("text", "")
                    if text:
                        print(f"You: {text}")
                        return text
