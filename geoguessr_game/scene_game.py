import pygame
import pandas as pd
import random
import time
import torch
from config import *
from base_scene import Scene
from prediction import Model # 替換成你的 AI 模型文件

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
        self.model = Model("model/model-19-1121.pth")   # 替換模型路徑
        self.font = pygame.font.SysFont(None, 28)
        self.random_row = None

    def on_enter(self):
        self.start_time = time.time()  # 每次進入場景重置開始時間
        self.result_timer = None
        self.player_answered = False  # 重置狀態
        self.model_answered = False
        self.player_choosen_city = None
        self.model_choosen_city = None
        self.player_score_feedback_timer = None
        self.model_score_feedback_timer = None
        self.load_images_and_options()

    def load_images_and_options(self):
        # load the pictures in data/256x256_global
        # step 1: from data/256x256_global/picture_coords.csv, choose an random 'index' and its corresponding 'image' and 'country'
        csv_path = "data/256x256_global/picture_coords.csv"
        picture_coords = pd.read_csv(csv_path)
        self.random_row = picture_coords.sample()  # 隨機選擇一行
        image_path = self.random_row['image'].values[0]  # 獲取圖片路徑
        country = self.random_row['country'].values[0]  # 獲取國家名稱
        # step 2: load the image from data/256x256_global/ + 'image' path
        full_image_path = f"data/256x256_global/{image_path}"
        # 載入並縮放圖片
        self.images = [
            pygame.transform.scale(pygame.image.load(full_image_path), (IMAGE_SIZE[0], IMAGE_SIZE[1]))
        ]
        # step 3: choose 4 random country from country_list
        # note: the correct answer should be in one of the 4 options
        self.city_options = [country]
        while len(self.city_options) < 4:
            random_country = country_list[random.randint(0, len(country_list) - 1)]
            if random_country not in self.city_options:
                self.city_options.append(random_country)
        random.shuffle(self.city_options)
        self.correct_city = country
        print("Correct city:", self.correct_city)

    def handle_player_choice(self, choice):
        if not self.player_answered:
            self.player_answered = True
            self.player_choosen_city = self.city_options[choice]
            print("Player choice:", self.player_choosen_city)
            if self.player_choosen_city == self.correct_city:
                print("Player Correct!")
            else:
                print("Player Wrong!")
            self.player_score_feedback_timer = (time.time(), "The player has made a guess")

    def handle_prediction_choice(self):
        # # 將圖片轉換為模型所需的格式並進行預測
        if not self.model_answered and self.time_left <= ROUND_TIME - 1:
            print("Handle prediction choice")
            # images_tensor = self.convert_images_to_tensor(self.images)
            prediction, probabilities = self.model.predict(f"data/256x256_global/{self.random_row['image'].values[0]}", self.city_options)
            self.model_choosen_city = prediction
            self.manager.model_probabilities = probabilities
            print("Model choice:", self.model_choosen_city)
            self.model_answered = True
            if self.model_choosen_city == self.correct_city:
                print("Model Correct!")
            else:
                print("Model Wrong!")
            self.model_score_feedback_timer = (time.time(), "The model has made a guess")

        #if not self.model_answered and self.time_left <= ROUND_TIME - 1:
        #    self.model_answered = True
        #    self.model_choosen_city = self.city_options[0]
        #    if self.model_choosen_city == self.correct_city:
        #        print("Model Correct!")
        #    else:
        #        print("Model Wrong!")
        #    self.model_score_feedback_timer = (time.time(), "The model has made a guess")


    def update(self):
        elapsed_time = time.time() - self.start_time
        self.time_left = max(ROUND_TIME - int(elapsed_time), 0)
        # 檢查玩家和模型是否都已作答，且設定 `result_timer`
        if self.player_answered and self.model_answered and not self.result_timer:
            self.result_timer = time.time() + 1.5
        # 檢查是否時間已到或需要進入結果場景
        if self.time_left == 0 or (self.result_timer and time.time() >= self.result_timer):
            self.move_to_result_scene()
        self.handle_prediction_choice()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # 顯示回合標題
        title_font = pygame.font.SysFont(None, 48)
        title_text = title_font.render(f"Round {self.manager.round_count}", True, (0, 0, 0))
        title_text_x, title_text_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 10 - 20
        title_text_rect = title_text.get_rect(center=(title_text_x, title_text_y))
        screen.blit(title_text, title_text_rect)

        # 顯示 player 和 model 分數
        player_score_text = self.font.render(f"Player Score: {self.manager.user_score}", True, (0, 0, 0))
        model_score_text = self.font.render(f"Model Score: {self.manager.model_score}", True, (0, 0, 0))
        player_score_x, player_score_y = 40, title_text_y + 90
        model_score_x, model_score_y = 40, title_text_y + 130
        screen.blit(player_score_text, (player_score_x, player_score_y))
        screen.blit(model_score_text, (model_score_x, model_score_y))

        # 顯示"The player has mades a guess"和"The model has mades a guess"
        # 顏色:(66, 112, 140)
        current_time = time.time()
        guess_font = pygame.font.SysFont(None, 30)
        if self.player_score_feedback_timer and current_time - self.player_score_feedback_timer[0] < 1:
            feedback_text = guess_font.render(self.player_score_feedback_timer[1], True, (66, 112, 140))
            screen.blit(feedback_text, (player_score_x + player_score_text.get_width() + 10, player_score_y))  # 顯示在玩家分數旁邊
        if self.model_score_feedback_timer and current_time - self.model_score_feedback_timer[0] < 1:
            feedback_text = guess_font.render(self.model_score_feedback_timer[1], True, (66, 112, 140))
            screen.blit(feedback_text, (model_score_x + model_score_text.get_width() + 10, model_score_y))  # 顯示在模型分數旁邊

        # 顯示倒數計時文字
        timer_text = self.font.render(f"Time Left: {self.time_left}", True, (0, 0, 0))
        screen.blit(timer_text, (WINDOW_WIDTH // 2 - timer_text.get_width() // 2, title_text_y + 20))

        # 倒數計時條
        bar_width = 300
        remaining_ratio = 1 - (time.time() - self.start_time) / ROUND_TIME
        remaining_bar_width = int(bar_width * remaining_ratio)
        bar_height = 20
        bar_x = WINDOW_WIDTH // 2 - bar_width // 2
        bar_y = title_text_y + 60
        pygame.draw.rect(screen, (209, 237, 225), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (2, 140, 106), (bar_x, bar_y, remaining_bar_width, bar_height))

        # 計算圖片位置
        image_x = (WINDOW_WIDTH - IMAGE_SIZE[0]) // 2
        image_y = title_text_y + 160
        screen.blit(self.images[0], (image_x, image_y))

        # 顯示提示文字
        hint_text = self.font.render("Guess the country based on the street view image", True, (0, 0, 0))
        screen.blit(hint_text, (WINDOW_WIDTH // 2 - hint_text.get_width() // 2, image_y + IMAGE_SIZE[1] + 20))

        # 設置按鈕位置
        self.button_width, self.button_height = 320, 50
        self.button_spacing = 20
        self.button_start_y = image_y + IMAGE_SIZE[1] + 60

        button_width, button_height = self.button_width, self.button_height
        button_spacing = self.button_spacing
        button_start_y = self.button_start_y

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
                button_color = (140, 140, 140)  # 加深選中的按鈕顏色
            elif button_rect.collidepoint(mouse_x, mouse_y):
                button_color = (170, 170, 170)  # 滑鼠懸停顏色
            else:
                button_color = (200, 200, 200)  # 預設顏色

            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            text = self.font.render(city, True, (0, 0, 0))
            screen.blit(text, (button_x + (button_width - text.get_width()) // 2,
                            button_y + (button_height - text.get_height()) // 2))

    def handle_events(self, events):
        button_width, button_height = self.button_width, self.button_height
        button_spacing = self.button_spacing
        button_start_y = self.button_start_y

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

    def convert_images_to_tensor(self, images):
        # 將 Pygame 圖片轉換為 Tensor 格式
        # 只有一張圖片，所以直接轉換即可
        #image_tensor = pygame.surfarray.array3d(images[0])
        #image_tensor = torch.from_numpy(image_tensor).permute(2, 0, 1).float() / 255.0
        #return image_tensor.unsqueeze(0)
        image_tensors = []
        for img in images:
            img_array = pygame.surfarray.array3d(img)  # 將圖片轉換為 numpy 陣列
            img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).float() / 255.0
            image_tensors.append(img_tensor)
        return torch.stack(image_tensors)  # 將多張圖片堆疊為一個 Tensor
