import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        
        # Caminho base para a pasta de sprites
        diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        pasta_sprites = os.path.join(diretorio_raiz, 'assets', 'imagens', 'sprites', 'player')        
        
        # 1. Carrega a imagem estática de referência
        self.image_parada = pygame.image.load(os.path.join(pasta_sprites, 'blue girl 1.png')).convert_alpha()
        
        self.largura_padrao = self.image_parada.get_width()
        self.altura_padrao = self.image_parada.get_height()
        self.tamanho_padrao = (self.largura_padrao, self.altura_padrao)

        # 2. Carrega a sprite de piscando
        caminho_piscando = os.path.join(pasta_sprites, 'blue girl piscando.png')
        if os.path.exists(caminho_piscando):
            self.image_piscando = pygame.transform.scale(
                pygame.image.load(caminho_piscando).convert_alpha(),
                self.tamanho_padrao
            )
        else:
            print(f"[AVISO] Arquivo não encontrado: {caminho_piscando}. Usando imagem padrão.")
            self.image_piscando = self.image_parada

        # 3. Frames de DIREITA
        self.frames_direita = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl direita ({i}).png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 5)
        ]
        
        # 4. Frames de ESQUERDA
        self.frames_esquerda = [
            pygame.transform.flip(frame, True, False) for frame in self.frames_direita
        ]

        # 5. Frames de CIMA
        self.frames_cima = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl cima {i}.png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 5)
        ]

        # 6. Frames de BAIXO
        self.frames_baixo = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl baixo {i}.png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 5)
        ]

        # 7. Frames de PULO (Direita)
        self.frames_pulo = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_sprites, f'blue girl jump {i}.png')).convert_alpha(),
                self.tamanho_padrao
            )
            for i in range(1, 3)
        ]

        # 8. Frames de PULO (Esquerda)
        self.frames_pulo_esquerda = [
            pygame.transform.flip(frame, True, False) for frame in self.frames_pulo
        ]
        
        # Estado inicial e Rect
        self.index_frame = 0
        self.image = self.image_parada
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        
        # Direção do jogador ('direita' ou 'esquerda')
        self.olhando_para = 'direita'

        # Física e Parâmetros de Movimento
        self.velocidade_animacao = 0.15
        self.velocidade_movimento = 4
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.gravidade = 0.8
        self.forca_pulo = -16
        self.no_chao = True
        self.chao_y = pos_y

        # Controle do tempo de piscada
        self.timer_piscada = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.velocidade_x = 0
        andou = False

        # --- MOVIMENTO NO CHÃO ---
        if self.no_chao:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocidade_x = self.velocidade_movimento
                self.rect.x += self.velocidade_x
                self.olhando_para = 'direita'  # Atualiza direção
                self.animar(self.frames_direita)
                andou = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocidade_x = -self.velocidade_movimento
                self.rect.x += self.velocidade_x
                self.olhando_para = 'esquerda'  # Atualiza direção
                self.animar(self.frames_esquerda)
                andou = True

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= self.velocidade_movimento
                if not andou:
                    self.animar(self.frames_cima)
                andou = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += self.velocidade_movimento
                if not andou:
                    self.animar(self.frames_baixo)
                andou = True

            # Animação da piscada (se estiver parado)
            if not andou:
                self.index_frame = 0
                self.timer_piscada += 1
                if 90 <= self.timer_piscada <= 100:
                    self.image = self.image_piscando
                else:
                    self.image = self.image_parada

                if self.timer_piscada > 100:
                    self.timer_piscada = 0

        # --- INÍCIO DO PULO ---
        if keys[pygame.K_SPACE] and self.no_chao:
            self.chao_y = self.rect.y  # Registra a posição Y inicial
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

        # --- FÍSICA E ANIMAÇÃO NO AR ---
        if not self.no_chao:
            # Controle de movimento horizontal no ar
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.velocidade_movimento
                self.olhando_para = 'direita'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= self.velocidade_movimento
                self.olhando_para = 'esquerda'

            self.velocidade_y += self.gravidade
            self.rect.y += self.velocidade_y
            
            # Atualiza o sprite do pulo de acordo com a direção que está olhando
            self.animar_pulo()

            # Pouso
            if self.rect.y >= self.chao_y:
                self.rect.y = self.chao_y
                self.velocidade_y = 0
                self.no_chao = True

    def animar(self, lista_frames):
        self.timer_piscada = 0
        self.index_frame += self.velocidade_animacao
        if self.index_frame >= len(lista_frames):
            self.index_frame = 0
        self.image = lista_frames[int(self.index_frame)]

    def animar_pulo(self):
        self.timer_piscada = 0
        
        # Escolhe a lista de frames certa dependendo de para onde ela está virada
        frames = self.frames_pulo if self.olhando_para == 'direita' else self.frames_pulo_esquerda
        
        # frame [0] = subindo, frame [1] = caindo
        if self.velocidade_y <= 0:
            self.image = frames[0]
        else:
            self.image = frames[1]