import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        
        # Caminho base para a pasta de sprites
        diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        pasta_sprites = os.path.join(diretorio_raiz, 'imagens', 'sprites')
        
        # 1. Carrega a imagem estática de referência para pegar a dimensão padrão
        self.image_parada = pygame.image.load(os.path.join(pasta_sprites, 'blue girl 1.png')).convert_alpha()
        
        # Obtém o tamanho (largura, altura) de referência das sprites do jogador
        self.largura_padrao = self.image_parada.get_width()
        self.altura_padrao = self.image_parada.get_height()
        self.tamanho_padrao = (self.largura_padrao, self.altura_padrao)

        # 2. Carrega e redimensiona os frames de DIREITA
        self.frames_direita = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl direita ({i}).png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 5)
        ]
        
        # 3. Gera a animação de ESQUERDA invertendo horizontalmente
        self.frames_esquerda = [
            pygame.transform.flip(frame, True, False) for frame in self.frames_direita
        ]

        # 4. Carrega e redimensiona os frames de CIMA
        self.frames_cima = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl cima {i}.png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 5)
        ]

        # 5. Carrega e redimensiona os frames de PULO (padronizando para o tamanho correto)
        self.frames_pulo = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl jump {i}.png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 4)
        ]
        
        # Estado inicial e Rect
        self.index_frame = 0
        self.image = self.image_parada
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        
        # Física e Parâmetros de Movimento
        self.velocidade_animacao = 0.15
        self.velocidade_movimento = 4
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.gravidade = 0.8
        self.forca_pulo = -13
        self.no_chao = True
        self.chao_y = pos_y  # Posição Y inicial como nível do chão

    def update(self):
        keys = pygame.key.get_pressed()
        self.velocidade_x = 0
        
        # --- MOVIMENTO HORIZONTAL ---
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocidade_x = self.velocidade_movimento
            self.rect.x += self.velocidade_x
            if self.no_chao:
                self.animar(self.frames_direita)
                
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocidade_x = -self.velocidade_movimento
            self.rect.x += self.velocidade_x
            if self.no_chao:
                self.animar(self.frames_esquerda)

        # --- MOVIMENTO VERTICAL (Andar para Cima) ---
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.no_chao:
                self.rect.y -= self.velocidade_movimento
                self.animar(self.frames_cima)

        elif self.no_chao:
            self.index_frame = 0
            self.image = self.image_parada

        # --- PULO (Espaço) ---
        if keys[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

        # --- APLICAÇÃO DA GRAVIDADE ---
        if not self.no_chao:
            self.velocidade_y += self.gravidade
            self.rect.y += self.velocidade_y
            self.animar_pulo()

            # Checagem simples de colisão com o chão
            if self.rect.y >= self.chao_y:
                self.rect.y = self.chao_y
                self.velocidade_y = 0
                self.no_chao = True

    def animar(self, lista_frames):
        self.index_frame += self.velocidade_animacao
        if self.index_frame >= len(lista_frames):
            self.index_frame = 0
        self.image = lista_frames[int(self.index_frame)]

    def animar_pulo(self):
        if self.velocidade_y < -3:
            self.image = self.frames_pulo[0]
        elif -3 <= self.velocidade_y <= 3:
            self.image = self.frames_pulo[1]
        else:
            self.image = self.frames_pulo[2]