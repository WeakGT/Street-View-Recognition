import pygame
import random

class ParticleSystem:
    def __init__(self, screen_width, screen_height, particle_count=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = [{"x": random.randint(0, screen_width), "y": random.randint(0, screen_height), 
                           "size": random.randint(2, 5), "speed": random.uniform(0.5, 2)} for _ in range(particle_count)]

    def update(self):
        """更新粒子的位置"""
        for particle in self.particles:
            particle["y"] -= particle["speed"]
            if particle["y"] < 0:  # 如果粒子超出畫面，重置到底部
                particle["y"] = self.screen_height
                particle["x"] = random.randint(0, self.screen_width)

    def draw(self, screen):
        """繪製粒子"""
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 255), (int(particle["x"]), int(particle["y"])), particle["size"])