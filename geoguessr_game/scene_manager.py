import pygame
from scene_start import StartScene
from scene_round_begin import RoundBeginScene
from scene_game import GameScene
from scene_result import ResultScene
from scene_final_result import FinalResultScene

class SceneManager:
    def __init__(self):
        #回合數
        self.round_count = 1
        #分數
        self.user_score = 0
        self.model_score = 0
        self.scenes = {
            "start": StartScene(self),
            "round_begin": RoundBeginScene(self),
            "game": GameScene(self),
            "result": ResultScene(self),
            "final_result": FinalResultScene(self)
        }
        self.current_scene = self.scenes["start"]

    def go_to(self, scene_name):
        self.current_scene = self.scenes[scene_name]
        if hasattr(self.current_scene, "on_enter"):
            self.current_scene.on_enter()  # 每次進入場景時重置時間

    def handle_events(self, events):
        self.current_scene.handle_events(events)

    def update(self):
        self.current_scene.update()

    def draw(self, screen):
        self.current_scene.draw(screen)
