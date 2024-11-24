import pygame
from base_scene import Scene
from config import *

class FinalResultScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        # 載入贏或輸的圖片
        self.win_image = pygame.image.load("geoguessr_game/assets/images/win.jpg")
        self.lose_image = pygame.image.load("geoguessr_game/assets/images/lose.png")
        self.draw_image = pygame.image.load("geoguessr_game/assets/images/draw.jpg")
        self.font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 36)
        # image resize as IMAGE_SIZE
        self.win_image = pygame.transform.scale(self.win_image, IMAGE_SIZE)
        self.lose_image = pygame.transform.scale(self.lose_image, IMAGE_SIZE)
        self.draw_image = pygame.transform.scale(self.draw_image, IMAGE_SIZE)
        self.exit_button_size = (200, 60)
        self.exit_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - self.exit_button_size[0] // 2,
                                            WINDOW_HEIGHT // 2 + 240, self.exit_button_size[0], self.exit_button_size[1])  # 按鈕大小與位置


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
            # 玩家贏
            screen.blit(self.win_image, (player_x - IMAGE_SIZE[0] // 2, player_y + 130))
            screen.blit(self.lose_image, (model_x - IMAGE_SIZE[0] // 2, model_y + 130))
        elif self.manager.user_score < self.manager.model_score:
            # 模型贏
            screen.blit(self.lose_image, (player_x - IMAGE_SIZE[0] // 2, player_y + 130))
            screen.blit(self.win_image, (model_x - IMAGE_SIZE[0] // 2, model_y + 130))
        else:
            # 平手
            screen.blit(self.draw_image, (player_x - IMAGE_SIZE[0] // 2, player_y + 130))
            screen.blit(self.draw_image, (model_x - IMAGE_SIZE[0] // 2, model_y + 130))
            

        # 繪製 Exit Game 按鈕
        # 顯示開始按鈕
        exit_button_text = self.font.render("Exit", True, (255, 255, 255))
        exit_button_color = (29, 106, 150) if not self.exit_button_rect.collidepoint(pygame.mouse.get_pos()) else (45, 135, 190)
        pygame.draw.rect(screen, exit_button_color, self.exit_button_rect, border_radius=10)
        screen.blit(exit_button_text, (
            self.exit_button_rect.x + (self.exit_button_rect.width - exit_button_text.get_width()) // 2,
            self.exit_button_rect.y + (self.exit_button_rect.height - exit_button_text.get_height()) // 2
        ))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button_rect.collidepoint(event.pos):
                    pygame.quit()  # 結束遊戲
                    exit()