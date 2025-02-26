import pygame
from config import *
from base_scene import Scene
from config import *

class ResultScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.Font(FONT_PATHS["default"], 32)
        self.alpha = 0  # 當前透明度
        self.fade_in = True  # 是否正在漸入

    def on_enter(self):
        # 接收來自 GameScene 的結果資料
        self.correct_city = self.manager.result_data["correct_city"]
        self.player_choice = self.manager.result_data["player_choice"]
        self.model_choice = self.manager.result_data["model_choice"]
        self.image_path = self.manager.result_data["image_path"]

        # 判斷玩家是否回答正確
        self.player_correct = self.player_choice == self.correct_city
        self.model_correct = self.model_choice == self.correct_city
        if self.player_correct:
            self.manager.user_score += 1
        if self.model_correct:
            self.manager.model_score += 1

        self.manager.results_data.append({
            "ID": len(self.manager.results_data) + 1,
            "Image Path":  self.image_path,
            "Player Choice": self.player_choice,
            "Model Choice": self.model_choice,
            "Correct Answer": self.correct_city,
            "Player Correct": int(self.player_correct),
            "Model Correct": int(self.model_correct)
        })

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.audio_manager.play_sound("click")
                if self.manager.round_count < NUM_ROUNDS:
                    self.manager.go_to("round_begin")
                else:
                    self.manager.go_to("final_result")

    def update(self):
        if self.fade_in:
            self.alpha += 10
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
        else:
            self.alpha -= 10
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_in = True

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # 顯示玩家的猜測結果是否正確
        model_probabilities = self.manager.model_probabilities
        player_result_text = f"Player: {'Correct' if self.player_correct else 'Incorrect'}"
        player_result_color = (167, 201, 87) if self.player_correct else (188, 71, 73)
        player_result_render = self.font.render(player_result_text, True, player_result_color)
        screen.blit(player_result_render, (WINDOW_WIDTH // 4 - player_result_render.get_width() // 2, WINDOW_HEIGHT // 2 - 300))
        player_guess_text = f"Player's Guess: {self.player_choice}"
        player_guess_render = self.font.render(player_guess_text, True, (0, 0, 0))
        screen.blit(player_guess_render, (WINDOW_WIDTH // 4 - player_guess_render.get_width() // 2, WINDOW_HEIGHT // 2 - 250))

        # 顯示模型的猜測結果是否正確
        model_result_text = f"Model: {'Correct' if self.model_correct else 'Incorrect'}"
        model_result_color = (167, 201, 87) if self.model_correct else (188, 71, 73)
        model_result_render = self.font.render(model_result_text, True, model_result_color)
        screen.blit(model_result_render, (WINDOW_WIDTH * 3 // 4 - model_result_render.get_width() // 2, WINDOW_HEIGHT // 2 - 300))
        model_guess_text = f"Model's Guess: {self.model_choice}"
        model_guess_render = self.font.render(model_guess_text, True, (0, 0, 0))
        screen.blit(model_guess_render, (WINDOW_WIDTH * 3 // 4 - model_guess_render.get_width() // 2, WINDOW_HEIGHT // 2 - 250))

        # 條形圖的屬性
        bar_width = 100  # 每個條形的寬度
        bar_spacing = 50  # 條形之間的間距
        max_bar_height = 300  # 條形的最大高度
        bar_x_start = (WINDOW_WIDTH - (len(model_probabilities) * (bar_width + bar_spacing) - bar_spacing)) // 2
        bar_y_base = WINDOW_HEIGHT // 2 + 160  # 條形圖的基準線

        # 顯示標題
        title_font = pygame.font.Font(FONT_PATHS["default"], 32)
        title_text = title_font.render("Model Prediction Probabilities", True, (0, 0, 0))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 2 - 160))

        # 繪製條形圖
        bar_font = pygame.font.Font(FONT_PATHS["default"], 20)
        for idx, (country, probability) in enumerate(model_probabilities.items()):
            # 計算條形位置與高度
            bar_height = int(probability * max_bar_height)  # 高度與機率成比例
            bar_x = bar_x_start + idx * (bar_width + bar_spacing)
            bar_y = bar_y_base - bar_height

            # 繪製條形
            pygame.draw.rect(screen, (66, 135, 245), (bar_x, bar_y, bar_width, bar_height))

            # 在條形上方顯示機率數字
            probability_text = bar_font.render(f"{probability * 100:.1f}%", True, (0, 0, 0))
            screen.blit(probability_text, (bar_x + (bar_width - probability_text.get_width()) // 2, bar_y - 35))

            # 在條形下方顯示選項名稱
            country_text = bar_font.render(country, True, (0, 0, 0))
            screen.blit(country_text, (bar_x + (bar_width - country_text.get_width()) // 2, bar_y_base + 10))

        # 顯示正確城市名稱
        correct_city_text = f"Country: {self.correct_city}"
        correct_city_render = self.font.render(correct_city_text, True, (0, 0, 0))
        screen.blit(correct_city_render, (WINDOW_WIDTH // 2 - correct_city_render.get_width() // 2, WINDOW_HEIGHT // 2 + 220))

        next_round_text = "Click to Next Round" if self.manager.round_count < NUM_ROUNDS else "Click to Check Result"
        next_round_font = pygame.font.SysFont(None, 48)
        text_render = next_round_font.render(next_round_text, True, (0, 0, 0))
        text_render.set_alpha(self.alpha)
        screen.blit(text_render, (WINDOW_WIDTH // 2 - text_render.get_width() // 2, WINDOW_HEIGHT // 2 + 280))
