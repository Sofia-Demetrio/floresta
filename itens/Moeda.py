import pygame
import os

class Moeda(pygame.sprite.Sprite):
    def __init__(self, pos_x_mundo, pos_y):
        super().__init__()
        
        diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        pasta_sprites = os.path.join(diretorio_raiz, 'assets', 'imagens', 'sprites')        

        
        # Define o novo tamanho da moeda em pixels (Largura, Altura)
        LARGURA_MOEDA = 45
        ALTURA_MOEDA = 45
        
        # Carrega os quadros da moeda e redimensiona cada um
        self.frames = []
        for i in range(1, 8):
            caminho_normal = os.path.join(pasta_sprites, f'moeda {i}.png')
            caminho_espaco = os.path.join(pasta_sprites, f'moeda {i} .png')
            
            img_original = None
            if os.path.exists(caminho_normal):
                img_original = pygame.image.load(caminho_normal).convert_alpha()
            elif os.path.exists(caminho_espaco):
                img_original = pygame.image.load(caminho_espaco).convert_alpha()

            if img_original:
                # Redimensiona a imagem para o tamanho desejado
                img_redimensionada = pygame.transform.scale(img_original, (LARGURA_MOEDA, ALTURA_MOEDA))
                self.frames.append(img_redimensionada)

        self.index_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        # Posição fixa no mundo virtual
        self.pos_x_mundo = pos_x_mundo
        self.rect.y = pos_y
        
        self.velocidade_animacao = 0.15

    def update(self, cam_x):
        # Atualiza a animação do giro
        self.index_frame += self.velocidade_animacao
        if self.index_frame >= len(self.frames):
            self.index_frame = 0
        self.image = self.frames[int(self.index_frame)]
        
        # Atualiza a posição na tela conforme o cenário/câmera se move
        self.rect.x = self.pos_x_mundo + cam_x