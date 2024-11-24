import pygame
from config import *
from base_scene import Scene
from config import *

class ResultScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 36)
        self.next_button_rect = None

    def on_enter(self):
        # 接收來自 GameScene 的結果資料
        self.correct_city = self.manager.result_data["correct_city"]
        self.player_choice = self.manager.result_data["player_choice"]
        self.model_choice = self.manager.result_data["model_choice"]

        # 判斷玩家是否回答正確
        self.player_correct = self.player_choice == self.correct_city
        self.model_correct = self.model_choice == self.correct_city
        if self.player_correct:
            self.manager.user_score += 1
        if self.model_correct:
            self.manager.model_score += 1

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.next_button_rect and self.next_button_rect.collidepoint(mouse_pos):
                    # 點擊按鈕後切換到下一回合
                    if self.manager.round_count < NUM_ROUNDS:
                        self.manager.go_to("round_begin")
                    else:
                        self.manager.go_to("final_result")

    def update(self):
        pass  # 此畫面不需要更新內容

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # 顯示玩家的猜測結果是否正確
        player_result_text = f"Player: {'Correct' if self.player_correct else 'Incorrect'}"
        player_result_color = (167, 201, 87) if self.player_correct else (188, 71, 73)
        player_result_render = self.font.render(player_result_text, True, player_result_color)
        screen.blit(player_result_render, (WINDOW_WIDTH // 4 - player_result_render.get_width() // 2, WINDOW_HEIGHT // 2 - 100))
        player_guess_text = f"Player's Guess: {self.player_choice}"
        player_guess_render = self.font.render(player_guess_text, True, (0, 0, 0))
        screen.blit(player_guess_render, (WINDOW_WIDTH // 4 - player_guess_render.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

        # 顯示模型的猜測結果是否正確
        model_result_text = f"Model: {'Correct' if self.model_correct else 'Incorrect'}"
        model_result_color = (167, 201, 87) if self.model_correct else (188, 71, 73)
        model_result_render = self.font.render(model_result_text, True, model_result_color)
        screen.blit(model_result_render, (WINDOW_WIDTH * 3 // 4 - model_result_render.get_width() // 2, WINDOW_HEIGHT // 2 - 100))
        model_guess_text = f"Model's Guess: {self.model_choice}"
        model_guess_render = self.font.render(model_guess_text, True, (0, 0, 0))
        screen.blit(model_guess_render, (WINDOW_WIDTH * 3 // 4 - model_guess_render.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

        # 顯示正確城市名稱
        correct_city_text = f"Country: {self.correct_city}"
        correct_city_render = self.font.render(correct_city_text, True, (0, 0, 0))
        screen.blit(correct_city_render, (WINDOW_WIDTH // 2 - correct_city_render.get_width() // 2, WINDOW_HEIGHT // 2 + 160))

        # 設置 "Next Round" 按鈕
        button_width = 320
        button_height = 60
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_y = WINDOW_HEIGHT // 2 + 200  # 按鈕位於底部
        self.next_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # 判斷滑鼠是否懸停在按鈕上
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.next_button_rect.collidepoint(mouse_x, mouse_y):
            button_color = (170, 170, 170)  # 滑鼠懸停顏色
        else:
            button_color = (200, 200, 200)  # 預設顏色

        pygame.draw.rect(screen, button_color, self.next_button_rect, border_radius=10)
        if self.manager.round_count < NUM_ROUNDS:
            button_text = self.button_font.render("Next Round", True, (0, 0, 0))
        else:
            button_text = self.button_font.render("Check Result", True, (0, 0, 0))
        screen.blit(
            button_text,
            (
                button_x + (button_width - button_text.get_width()) // 2,
                button_y + (button_height - button_text.get_height()) // 2,
            ),
        )
