import pygame
import random
import torch
from config import *
from prediction import Model  # 替換成你的 AI 模型文件

class Game:
    def __init__(self, window):
        self.window = window
        self.user_score = 0
        self.model_score = 0
        self.current_round = 1
        self.time_left = ROUND_TIME
        self.correct_city = None
        self.model = Model("path/to/your/model.pth")  # 替換模型路徑
        self.load_images_and_options()
        self.font = pygame.font.SysFont(None, 36)  # 字體
        self.points_display = ""  # 加分顯示文本
        self.points_display_timer = None  # 控制加分顯示的計時器
        self.model_points_display = ""  # 模型加分顯示文本
        self.model_points_display_timer = None  # 模型加分顯示計時器

    def load_images_and_options(self):
        # 載入四張圖片和四個城市選項
        self.images = [
            pygame.transform.scale(pygame.image.load("assets/images/image1.jpg"), (IMAGE_SIZE[0], IMAGE_SIZE[1])),
            pygame.transform.scale(pygame.image.load("assets/images/image2.jpg"), (IMAGE_SIZE[0], IMAGE_SIZE[1])),
            pygame.transform.scale(pygame.image.load("assets/images/image3.jpg"), (IMAGE_SIZE[0], IMAGE_SIZE[1])),
            pygame.transform.scale(pygame.image.load("assets/images/image4.jpg"), (IMAGE_SIZE[0], IMAGE_SIZE[1]))
        ]
        self.city_options = ["City1", "City2", "City3", "City4"]  # 替換城市名稱
        self.correct_city = self.city_options[0]  # 假設正確答案總是第一個選項
        self.player_answered = False
        self.model_answered = False
        self.result_timer = None
        
        button_width, button_height, button_spacing = 400, 40, 20
        total_image_height = 2 * IMAGE_SIZE[1] + 10
        button_start_y = int(WINDOW_HEIGHT * 0.15) + total_image_height + 30

        self.buttons = []  # 初始化按鈕列表
        for i in range(4):
            button_x = (WINDOW_WIDTH - button_width) // 2
            button_y = button_start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.buttons.append(button_rect)

    def handle_player_choice(self, choice):
        if not self.player_answered:  # 確保玩家只回答一次
            self.player_answered = True
            points = 0
            if choice == self.correct_city:
                points = int(200 * round(self.time_left / ROUND_TIME, 1))
                self.user_score += points
                self.points_display = f"+{points}"
                print("Correct!")
            else:
                print("Wrong answer!")
            self.points_display_timer = pygame.time.get_ticks()
            self.result_timer = pygame.time.get_ticks()  # 設置結果顯示計時器

    def handle_prediction_choice(self):
        # # 將圖片轉換為模型所需的格式並進行預測
        # images_tensor = self.convert_images_to_tensor(self.images)
        # prediction = self.model.predict(images_tensor)
        # # 假設模型正確，計算模型的分數
        # if prediction == self.correct_city:
        #     points = int(200 * round(self.time_left / ROUND_TIME, 1))
        #     self.model_score += points
        # return prediction
    
        if not self.model_answered and self.time_left <= ROUND_TIME - 1:
            self.model_answered = True
            if self.correct_city == self.city_options[0]:  # 模型選擇第一個選項
                points = int(200 * round(self.time_left / ROUND_TIME, 1))
                self.model_score += points
                self.model_points_display = f"+{points}"

            self.model_points_display_timer = pygame.time.get_ticks()

    def update(self):
        self.time_left -= 1 / 30  # 假設 FPS = 30
        if self.time_left <= 0:
            self.time_left = 0
            if not self.result_timer:  # 如果尚未設置結果計時器
                self.result_timer = pygame.time.get_ticks()

        self.handle_prediction_choice()  # 處理模型選擇

        if self.result_timer:
            elapsed_time = pygame.time.get_ticks() - self.result_timer
            if elapsed_time >= 1000:  # 等待 1 秒後進入下一題
                self.next_round()

        if self.points_display_timer:
            elapsed_time = pygame.time.get_ticks() - self.points_display_timer
            if elapsed_time >= 1000:  # 加分文本顯示 1 秒後消失
                self.points_display = ""
                self.points_display_timer = None
            
        if self.model_points_display_timer:
            elapsed_time = pygame.time.get_ticks() - self.model_points_display_timer
            if elapsed_time >= 1000:  # 模型加分文本顯示 1 秒後消失
                self.model_points_display = ""
                self.model_points_display_timer = None

    def render(self):
        # 渲染背景
        self.window.fill((255, 255, 255))

        # 計算圖片的擺放位置，確保圖片在窗口範圍內
        image_width, image_height = IMAGE_SIZE[0], IMAGE_SIZE[1]
        total_image_width = 2 * image_width + (2 - 1) * 10  # 兩張圖片之間的間距為 10 像素
        total_image_height = 2 * image_height + 10

        start_x = (WINDOW_WIDTH - total_image_width) // 2
        start_y = int(WINDOW_HEIGHT * 0.15)  # 調整到中間偏上

        # 渲染四張圖片（兩行兩列）
        for i, img in enumerate(self.images):
            x = start_x + (i % 2) * (image_width + 10)  # 每行兩張圖片
            y = start_y + (i // 2) * (image_height + 10)  # 每列兩張圖片
            self.window.blit(img, (x, y))

        # 顯示當前回合和倒計時（在窗口正中間）
        round_text = self.font.render(f"Round: {self.current_round}", True, (0, 0, 0))
        time_text = self.font.render(f"{int(self.time_left)}", True, (0, 0, 0))
        self.window.blit(round_text, (WINDOW_WIDTH // 2 - round_text.get_width() // 2, 10))
        self.window.blit(time_text, (WINDOW_WIDTH // 2 - time_text.get_width() // 2, 50))

        # 顯示分數（左邊顯示玩家分數，右邊顯示模型分數）
        user_score_text = self.font.render(f"User: {self.user_score}", True, (0, 0, 0))
        model_score_text = self.font.render(f"Model: {self.model_score}", True, (0, 0, 0))
        self.window.blit(user_score_text, (10, 10))
        self.window.blit(model_score_text, (WINDOW_WIDTH - model_score_text.get_width() - 10, 10))

        # 分數顯示條
        bar_width = 20
        bar_height = 300
        bar_x_user = 50
        bar_x_model = WINDOW_WIDTH - bar_x_user - bar_width
        bottom_height = 35
        max_score = 2000  # 假設最大分數

        # 用戶分數條
        user_bar_height = int((self.user_score / max_score) * bar_height)
        pygame.draw.rect(self.window, (0, 0, 255), (bar_x_user, WINDOW_HEIGHT - bar_height - bottom_height, bar_width, bar_height), border_radius=5)
        pygame.draw.rect(self.window, (0, 255, 0), (bar_x_user, WINDOW_HEIGHT - user_bar_height - bottom_height, bar_width, user_bar_height), border_radius=5)

        if self.points_display:
            points_text = self.font.render(self.points_display, True, (0, 0, 0))
            self.window.blit(points_text, (bar_x_user + bar_width // 2 - points_text.get_width() // 2, WINDOW_HEIGHT - bar_height - bottom_height - 30))
        
        if self.model_points_display:
            model_points_text = self.font.render(self.model_points_display, True, (0, 0, 0))
            self.window.blit(model_points_text, (bar_x_model + bar_width // 2 - model_points_text.get_width() // 2, WINDOW_HEIGHT - bar_height - bottom_height - 30))

        # 模型分數條
        model_bar_height = int((self.model_score / max_score) * bar_height)
        pygame.draw.rect(self.window, (0, 0, 255), (bar_x_model, WINDOW_HEIGHT - bar_height - bottom_height, bar_width, bar_height), border_radius=5)
        pygame.draw.rect(self.window, (255, 0, 0), (bar_x_model, WINDOW_HEIGHT - model_bar_height - bottom_height, bar_width, model_bar_height), border_radius=5)

        # 渲染選項按鈕
        button_width = 400
        button_height = 40
        button_spacing = 20
        button_start_y = start_y + total_image_height + 30

        for i, city in enumerate(self.city_options):
            button_x = (WINDOW_WIDTH - button_width) // 2
            button_y = button_start_y + i * (button_height + button_spacing)
            button_y = button_start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.window, (200, 200, 200), button_rect, border_radius=10)
            pygame.draw.rect(self.window, (150, 150, 150), button_rect, 3, border_radius=10)
            text = self.font.render(city, True, (0, 0, 0))
            self.window.blit(text, (button_x + (button_width - text.get_width()) // 2, button_y + (button_height - text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.player_answered:
            mouse_pos = event.pos
            for i, button in enumerate(self.buttons):
                if button.collidepoint(mouse_pos):
                    self.handle_player_choice(self.city_options[i])

    def next_round(self):
        if self.current_round < NUM_ROUNDS:
            self.current_round += 1
            self.time_left = ROUND_TIME
            self.load_images_and_options()
        else:
            self.end_game()
    
    def end_game(self):
        # 遊戲結束時顯示最終分數
        print("Game Over! User Score: ", self.user_score, "Model Score: ", self.model_score)
        pygame.quit()

    def convert_images_to_tensor(self, images):
        # 將 Pygame 圖片轉換為 Tensor 格式
        image_tensors = []
        for img in images:
            img_array = pygame.surfarray.array3d(img)  # 將圖片轉換為 numpy 陣列
            img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).float() / 255.0
            image_tensors.append(img_tensor)
        return torch.stack(image_tensors)  # 將多張圖片堆疊為一個 Tensor