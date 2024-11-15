import pygame
from base_scene import Scene
from config import *

class FinalResultScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("Final Result", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 300))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.text, self.text_rect)