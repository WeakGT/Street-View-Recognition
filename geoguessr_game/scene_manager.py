import pygame
from scene_start import StartScene
from scene_round_begin import RoundBeginScene
from scene_game import GameScene
from scene_result import ResultScene
from scene_final_result import FinalResultScene
import os, csv

class SceneManager:
    def __init__(self):
        #回合數
        self.round_count = 0
        #分數
        self.user_score = 0
        self.model_score = 0
        self.results_data = []
        self.results_file = "./result/log.csv"
        # 檢查結果文件是否存在，如果不存在則創建並寫入標題行
        if not os.path.exists(self.results_file):
            dir = os.path.dirname(self.results_file)
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(self.results_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Player Choice", "Model Choice", "Correct Answer", "Player Correct", "Model Correct"])

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
