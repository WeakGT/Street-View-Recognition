import pygame
from base_scene import Scene
from config import *
import csv

class FinalResultScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        # 載入贏或輸的圖片
        self.win_image = pygame.image.load("geoguessr_game/assets/images/win.jpg")
        self.lose_image = pygame.image.load("geoguessr_game/assets/images/lose.png")
        self.draw_image = pygame.image.load("geoguessr_game/assets/images/draw.jpg")
        self.font = pygame.font.Font(FONT_PATHS["default"], 36)
        # 圖片 resize
        self.win_image = pygame.transform.scale(self.win_image, IMAGE_SIZE)
        self.lose_image = pygame.transform.scale(self.lose_image, IMAGE_SIZE)
        self.draw_image = pygame.transform.scale(self.draw_image, IMAGE_SIZE)
        
        # 按鈕大小與位置
        self.button_size = (200, 60)
        self.exit_button_rect = pygame.Rect(
            WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 + 240, *self.button_size
        )
        self.restart_button_rect = pygame.Rect(
            WINDOW_WIDTH // 2 + 50, WINDOW_HEIGHT // 2 + 240, *self.button_size
        )

    def on_enter(self):
        self.audio_manager.pause_music()
        self.audio_manager.play_sound("ending")
        sound_length = self.audio_manager.get_sound_length("ending")
        pygame.time.set_timer(pygame.USEREVENT, int(sound_length * 1000) + 500)

        # 儲存結果到 CSV
        results_file = "./result/log.csv"
        with open(results_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Player Choice", "Model Choice", "Correct Answer", "Player Correct", "Model Correct"])
            writer.writerows(self.manager.results_data)

    def draw(self, screen):
        # 清空畫面
        screen.fill((255, 255, 255))

        # 顯示分數
        player_score_text = self.font.render(f"Player Score: {self.manager.user_score}", True, (0, 0, 0))
        model_score_text = self.font.render(f"Model Score: {self.manager.model_score}", True, (0, 0, 0))
        playr_accuracy_text = self.font.render(f"Accuracy: {self.manager.user_score / NUM_ROUNDS * 100:.2f}%", True, (0, 0, 0))
        model_accuracy_text = self.font.render(f"Accuracy: {self.manager.model_score / NUM_ROUNDS * 100:.2f}%", True, (0, 0, 0))
        
        # 分數顯示位置
        player_x, player_y = WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 - 200
        model_x, model_y = WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT // 2 - 200
        
        screen.blit(player_score_text, (player_x  - player_score_text.get_width() // 2, player_y))
        screen.blit(model_score_text, (model_x - model_score_text.get_width() // 2 , model_y))
        screen.blit(playr_accuracy_text, (player_x - playr_accuracy_text.get_width() // 2, player_y + 60))
        screen.blit(model_accuracy_text, (model_x - model_accuracy_text.get_width() // 2, model_y + 60))

        # 判斷贏家和輸家
        if self.manager.user_score > self.manager.model_score:
            screen.blit(self.win_image, (player_x - IMAGE_SIZE[0] // 2, player_y + 130))
            screen.blit(self.lose_image, (model_x - IMAGE_SIZE[0] // 2, model_y + 130))
        elif self.manager.user_score < self.manager.model_score:
            screen.blit(self.lose_image, (player_x - IMAGE_SIZE[0] // 2, player_y + 130))
            screen.blit(self.win_image, (model_x - IMAGE_SIZE[0] // 2, model_y + 130))
        else:
            screen.blit(self.draw_image, (player_x - IMAGE_SIZE[0] // 2, player_y + 130))
            screen.blit(self.draw_image, (model_x - IMAGE_SIZE[0] // 2, model_y + 130))

        # 繪製 Exit 按鈕
        exit_button_text = self.font.render("Exit", True, (255, 255, 255))
        exit_button_color = (200, 50, 50) if not self.exit_button_rect.collidepoint(pygame.mouse.get_pos()) else (255, 70, 70)
        pygame.draw.rect(screen, exit_button_color, self.exit_button_rect, border_radius=10)
        screen.blit(exit_button_text, (
            self.exit_button_rect.x + (self.exit_button_rect.width - exit_button_text.get_width()) // 2,
            self.exit_button_rect.y + (self.exit_button_rect.height - exit_button_text.get_height()) // 2
        ))

        # 繪製 Restart 按鈕
        restart_button_text = self.font.render("Restart", True, (255, 255, 255))
        restart_button_color = (29, 106, 150) if not self.restart_button_rect.collidepoint(pygame.mouse.get_pos()) else (45, 135, 190)
        pygame.draw.rect(screen, restart_button_color, self.restart_button_rect, border_radius=10)
        screen.blit(restart_button_text, (
            self.restart_button_rect.x + (self.restart_button_rect.width - restart_button_text.get_width()) // 2,
            self.restart_button_rect.y + (self.restart_button_rect.height - restart_button_text.get_height()) // 2
        ))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button_rect.collidepoint(event.pos):
                    self.audio_manager.play_sound("click")
                    pygame.quit()
                    exit()
                elif self.restart_button_rect.collidepoint(event.pos):
                    self.audio_manager.play_sound("click")
                    self.audio_manager.resume_music()
                    self.manager.reset()
            elif event.type == pygame.USEREVENT:
                self.audio_manager.resume_music()
                pygame.time.set_timer(pygame.USEREVENT, 0)