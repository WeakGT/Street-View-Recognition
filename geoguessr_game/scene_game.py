import pygame
import time
from config import *
from base_scene import Scene
# from prediction import Model  # 替換成你的 AI 模型文件

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        # 時間
        self.time_left = ROUND_TIME
        self.start_time = time.time()
        self.result_timer = None
        # 回答
        self.player_answered = False
        self.model_answered = False
        self.player_choosen_city = None
        self.model_choosen_city = None
        self.correct_city = None
        self.model_guess_correct = False
        # 顯示分數變化的計時器
        self.player_score_feedback_timer = None
        self.model_score_feedback_timer = None
        # 模型
        # self.model = Model("path/to/your/model.pth")  # 替換模型路徑
        # 畫面
        self.load_images_and_options()
        self.font = pygame.font.SysFont(None, 40)

    def on_enter(self):
        self.start_time = time.time()  # 每次進入場景重置開始時間
        self.result_timer = None
        self.player_answered = False  # 重置狀態
        self.model_answered = False
        self.player_choosen_city = None
        self.model_choosen_city = None
        self.correct_city = None
        self.player_score_feedback_timer = None
        self.model_score_feedback_timer = None

    def load_images_and_options(self):
        # 載入並縮放圖片
        self.images = [
            pygame.transform.scale(pygame.image.load("assets/images/image1.jpg"), (IMAGE_SIZE[0], IMAGE_SIZE[1]))
        ]
        self.city_options = ["City1", "City2", "City3", "City4"]
        self.correct_city = self.city_options[0]  # 正確答案假設為第一個選項

    def handle_player_choice(self, choice):
        if not self.player_answered:
            self.player_answered = True
            self.player_choosen_city = self.city_options[choice]
            if self.player_choosen_city == self.correct_city:
                self.manager.user_score += 1
                self.player_score_feedback_timer = (time.time(), "+1")
            else:
                self.player_score_feedback_timer = (time.time(), "+0")
            self.result_timer = time.time() + 1.5

    def handle_prediction_choice(self):
        if not self.model_answered and self.time_left <= ROUND_TIME - 1:
            self.model_answered = True
            self.model_choosen_city = self.city_options[0]
            if self.model_choosen_city == self.correct_city:
                self.manager.model_score += 1
                self.model_score_feedback_timer = (time.time(), "+1")
            else:
                self.model_score_feedback_timer = (time.time(), "+0")


    def update(self):
        elapsed_time = time.time() - self.start_time
        self.time_left = max(ROUND_TIME - int(elapsed_time), 0)
        if self.time_left == 0 or (self.result_timer and time.time() >= self.result_timer):
            self.move_to_result_scene()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # 顯示 player 和 model 分數
        player_score_text = self.font.render(f"Player Score: {self.manager.user_score}", True, (0, 0, 0))
        model_score_text = self.font.render(f"Model Score: {self.manager.model_score}", True, (0, 0, 0))
        screen.blit(player_score_text, (320, 220))
        screen.blit(model_score_text, (320, 260))

        # 顯示 "+1" 或 "+0" 標記，若在一秒內則顯示
        current_time = time.time()
        if self.player_score_feedback_timer and current_time - self.player_score_feedback_timer[0] < 1:
            feedback_text = self.font.render(self.player_score_feedback_timer[1], True, (0, 128, 0))
            screen.blit(feedback_text, (540, 220))  # 顯示在玩家分數旁邊
        if self.model_score_feedback_timer and current_time - self.model_score_feedback_timer[0] < 1:
            feedback_text = self.font.render(self.model_score_feedback_timer[1], True, (0, 128, 0))
            screen.blit(feedback_text, (540, 260))  # 顯示在模型分數旁邊

        # 計算圖片位置
        image_x = (WINDOW_WIDTH - IMAGE_SIZE[0]) // 2
        image_y = int(WINDOW_HEIGHT * 0.2) + 140
        screen.blit(self.images[0], (image_x, image_y))

        # 顯示倒數計時文字
        timer_text = self.font.render(f"Time Left: {self.time_left}", True, (0, 0, 0))
        screen.blit(timer_text, (WINDOW_WIDTH // 2 - timer_text.get_width() // 2, 270))

        # 倒數計時條
        bar_width = 300
        remaining_ratio = 1 - (time.time() - self.start_time) / ROUND_TIME
        remaining_bar_width = int(bar_width * remaining_ratio)
        bar_height = 20
        bar_x = WINDOW_WIDTH // 2 - bar_width // 2
        bar_y = 300
        pygame.draw.rect(screen, (209, 237, 225), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (2, 140, 106), (bar_x, bar_y, remaining_bar_width, bar_height))

        # 顯示回合標題
        title_font = pygame.font.SysFont(None, 70)
        title_text = title_font.render(f"Round {self.manager.round_count}", True, (0, 0, 0))
        title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 220))
        screen.blit(title_text, title_text_rect)

        # 顯示提示文字
        hint_text = self.font.render("Guess the city based on the street view image", True, (0, 0, 0))
        screen.blit(hint_text, (WINDOW_WIDTH // 2 - hint_text.get_width() // 2, image_y + IMAGE_SIZE[1] + 20))

        # 設置按鈕位置
        button_width = 400
        button_height = 50
        button_spacing = 20
        button_start_y = image_y + IMAGE_SIZE[1] + 60

        # 顯示按鈕
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, city in enumerate(self.city_options):
            row = i // 2
            col = i % 2
            button_x = (WINDOW_WIDTH - 2 * button_width - button_spacing) // 2 + col * (button_width + button_spacing)
            button_y = button_start_y + row * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # 判斷按鈕顏色
            if city == self.player_choosen_city:
                button_color = (170, 170, 170)  # 加深選中的按鈕顏色
            elif button_rect.collidepoint(mouse_x, mouse_y):
                button_color = (170, 170, 170)  # 滑鼠懸停顏色
            else:
                button_color = (200, 200, 200)  # 預設顏色

            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            text = self.font.render(city, True, (0, 0, 0))
            screen.blit(text, (button_x + (button_width - text.get_width()) // 2,
                            button_y + (button_height - text.get_height()) // 2))

    def handle_events(self, events):
        button_width = 400
        button_height = 50
        button_spacing = 20
        button_start_y = int(WINDOW_HEIGHT * 0.2) + 140 + IMAGE_SIZE[1] + 60

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.player_answered:
                mouse_pos = event.pos

                for i in range(len(self.city_options)):
                    row = i // 2
                    col = i % 2
                    button_x = (WINDOW_WIDTH - 2 * button_width - button_spacing) // 2 + col * (button_width + button_spacing)
                    button_y = button_start_y + row * (button_height + button_spacing)
                    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                    if button_rect.collidepoint(mouse_pos):
                        self.handle_player_choice(i)
                        break

    def move_to_result_scene(self):
        self.manager.result_data = {
            "correct_city": self.correct_city,
            "player_choice": self.player_choosen_city,
            "model_choice": self.model_choosen_city,
        }
        self.manager.go_to("result")
