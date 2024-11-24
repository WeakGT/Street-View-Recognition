import pygame
from audio_manager import AudioManager

# 定義場景基底類別
class Scene:
    def __init__(self, manager):
        self.manager = manager
        self.audio_manager = AudioManager()
        effects = ["click", "ending"]
        for effect in effects:
            self.audio_manager.load_sound(effect, f"geoguessr_game/assets/audio/effects/{effect}.wav")

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass