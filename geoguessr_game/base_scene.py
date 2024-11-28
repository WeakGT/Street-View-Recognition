import pygame
from config import *
from audio_manager import AudioManager
from particle import ParticleSystem

# 定義場景基底類別
class Scene:
    def __init__(self, manager):
        self.manager = manager
        self.audio_manager = AudioManager()
        self.particle_system = ParticleSystem(WINDOW_WIDTH, WINDOW_HEIGHT, particle_count=100)
        self.background_image = pygame.image.load("geoguessr_game/assets/images/world_map.png")
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        effects = ["click", "ending"]
        for effect in effects:
            self.audio_manager.load_sound(effect, f"geoguessr_game/assets/audio/effects/{effect}.wav")

    def handle_events(self, events):
        pass

    def update(self):
        self.particle_system.update()

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        self.particle_system.draw(screen)