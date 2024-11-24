import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}  # 用於存放音效
        self.music_volume = 0.5  # 背景音樂音量
        self.sound_volume = 0.5  # 音效音量

    def load_music(self, music_path):
        """加載並播放背景音樂"""
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        """停止背景音樂"""
        pygame.mixer.music.stop()

    def pause_music(self):
        """暫停播放背景音樂"""
        pygame.mixer.music.pause()

    def resume_music(self):
        """繼續播放背景音樂"""
        pygame.mixer.music.unpause()

    def load_sound(self, sound_name, sound_path):
        """加載音效"""
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(self.sound_volume)
        self.sounds[sound_name] = sound

    def play_sound(self, sound_name):
        """播放指定的音效"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def get_sound_length(self, sound_name):
        """獲取音效的長度"""
        return self.sounds[sound_name].get_length() if sound_name in self.sounds else 0

    def set_music_volume(self, volume):
        """設置背景音樂音量"""
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """設置音效音量"""
        self.sound_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)