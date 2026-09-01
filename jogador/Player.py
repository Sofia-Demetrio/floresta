import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        
        # Caminho base para a pasta de sprites
        diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        pasta_sprites = os.path.join(diretorio_raiz, 'imagens', 'sprites')
        
        self.frames_direita = [
            pygame.image.load(os.path.join(pasta_sprites, 'blue girl direita (1).png')).convert_alpha(),
            pygame.image.load(os.path.join(pasta_sprites, 'blue girl direita (2).png')).convert_alpha(),
            pygame.image.load(os.path.join(pasta_sprites, 'blue girl direita (3).png')).convert_alpha(),
            pygame.image.load(os.path.join(pasta_sprites, 'blue girl direita (4).png')).convert_alpha(),
        ]
        
        self.frames_esquerda = [
            pygame.transform.flip(frame, True, False) for frame in self.frames_direita
        ]
        
        self.image_parada = pygame.image.load(os.path.join(pasta_sprites, 'blue girl 1.png')).convert_alpha()
        
        # Estado inicial
        self.index_frame = 0
        self.image = self.image_parada
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        
        self.velocidade_animacao = 0.15
        self.velocidade_movimento = 3

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movimento para a direita 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidade_movimento
            self.animar_direita()
            
        # Movimento para a esquerda
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidade_movimento
            self.animar_esquerda()
            
        else:
            self.index_frame = 0
            self.image = self.image_parada

    def animar_direita(self):
        self.index_frame += self.velocidade_animacao
        if self.index_frame >= len(self.frames_direita):
            self.index_frame = 0
        self.image = self.frames_direita[int(self.index_frame)]

    def animar_esquerda(self):
        self.index_frame += self.velocidade_animacao
        if self.index_frame >= len(self.frames_esquerda):
            self.index_frame = 0
        self.image = self.frames_esquerda[int(self.index_frame)]