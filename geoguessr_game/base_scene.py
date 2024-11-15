import pygame

# 定義場景基底類別
class Scene:
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass