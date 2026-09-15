import os
import pygame


class Player(pygame.sprite.Sprite):

  def __init__(self, pos_x, pos_y):
    super().__init__()

    # Caminho base para a pasta de sprites
    diretorio_raiz = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
    pasta_sprites = os.path.join(
        diretorio_raiz, 'assets', 'imagens', 'sprites', 'player'
    )

    # 1. Carrega a imagem estática de referência
    self.image_parada = pygame.image.load(
        os.path.join(pasta_sprites, 'blue girl 1.png')
    ).convert_alpha()

    self.largura_padrao = self.image_parada.get_width()
    self.altura_padrao = self.image_parada.get_height()
    self.tamanho_padrao = (self.largura_padrao, self.altura_padrao)

    # 2. Carrega a sprite de piscando
    caminho_piscando = os.path.join(pasta_sprites, 'blue girl piscando.png')
    if os.path.exists(caminho_piscando):
      self.image_piscando = pygame.transform.scale(
          pygame.image.load(caminho_piscando).convert_alpha(),
          self.tamanho_padrao,
      )
    else:
      self.image_piscando = self.image_parada

    # 3. Frames de DIREITA
    self.frames_direita = [
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(pasta_sprites, f'blue girl direita ({i}).png')
            ).convert_alpha(),
            self.tamanho_padrao,
        )
        for i in range(1, 5)
    ]

    # 4. Frames de ESQUERDA
    self.frames_esquerda = [
        pygame.transform.flip(frame, True, False)
        for frame in self.frames_direita
    ]

    # 5. Frames de CIMA
    self.frames_cima = [
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(pasta_sprites, f'blue girl cima {i}.png')
            ).convert_alpha(),
            self.tamanho_padrao,
        )
        for i in range(1, 5)
    ]

    # 6. Frames de BAIXO
    self.frames_baixo = [
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(pasta_sprites, f'blue girl baixo {i}.png')
            ).convert_alpha(),
            self.tamanho_padrao,
        )
        for i in range(1, 5)
    ]

    # 7. Frames de PULO (Direita)
    self.frames_pulo = [
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(pasta_sprites, f'blue girl jump {i}.png')
            ).convert_alpha(),
            self.tamanho_padrao,
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

    # --- SITEMA DE GLITCH / IN VULNERABILIDADE ---
    self.invulneravel = False
    self.tempo_invulneravel = 0
    self.duracao_glitch = 60  # Duração em frames (~1 segundo a 60 FPS)

  def levar_dano(self):
    """Ativa o estado de invulnerabilidade e o efeito visual de glitch."""
    if not self.invulneravel:
      self.invulneravel = True
      self.tempo_invulneravel = self.duracao_glitch

      # Leve recuo/empurrão ao tomar dano (Knockback)
      if self.olhando_para == 'direita':
        self.rect.x -= 20
      else:
        self.rect.x += 20

      # Pulo leve de reação ao dano
      self.velocidade_y = -6
      self.no_chao = False

  def aplicar_efeito_glitch(self):
    """Alterna a transparência da imagem para criar o piscar (glitch)."""
    if self.invulneravel:
      self.tempo_invulneravel -= 1

      # Alterna a visibilidade a cada 4 frames para dar o piscar
      if (self.tempo_invulneravel // 4) % 2 == 0:
        self.image.set_alpha(80)  # Fica parcialmente transparente
      else:
        self.image.set_alpha(255)  # Fica opaco normal

      # Finaliza o efeito
      if self.tempo_invulneravel <= 0:
        self.invulneravel = False
        self.image.set_alpha(255)
    else:
      self.image.set_alpha(255)

  def update(self):
    keys = pygame.key.get_pressed()
    self.velocidade_x = 0
    andou_horizontal = False
    andou_vertical = False

    # --- CONTROLE HORIZONTAL ---
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.velocidade_x = self.velocidade_movimento
      self.rect.x += self.velocidade_x
      self.olhando_para = 'direita'
      andou_horizontal = True
      if self.no_chao:
        self.animar(self.frames_direita)

    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.velocidade_x = -self.velocidade_movimento
      self.rect.x += self.velocidade_x
      self.olhando_para = 'esquerda'
      andou_horizontal = True
      if self.no_chao:
        self.animar(self.frames_esquerda)

    # --- MOVIMENTO VERTICAL ---
    if self.no_chao:
      if keys[pygame.K_UP] or keys[pygame.K_w]:
        self.rect.y -= self.velocidade_movimento
        andou_vertical = True
        if not andou_horizontal:
          self.animar(self.frames_cima)

      elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        self.rect.y += self.velocidade_movimento
        andou_vertical = True
        if not andou_horizontal:
          self.animar(self.frames_baixo)

      # Animação de piscar natural dos olhos quando parada
      if not andou_horizontal and not andou_vertical:
        self.index_frame = 0
        self.timer_piscada += 1
        if 90 <= self.timer_piscada <= 100:
          self.image = self.image_piscando
        else:
          self.image = self.image_parada

        if self.timer_piscada > 100:
          self.timer_piscada = 0

      # --- INÍCIO DO PULO ---
      if keys[pygame.K_SPACE]:
        self.chao_y = self.rect.y
        self.velocidade_y = self.forca_pulo
        self.no_chao = False

    # --- FÍSICA E ANIMAÇÃO NO AR ---
    else:
      self.velocidade_y += self.gravidade
      self.rect.y += self.velocidade_y
      self.animar_pulo()

      if self.rect.y >= self.chao_y:
        self.rect.y = self.chao_y
        self.velocidade_y = 0
        self.no_chao = True

    # Aplica a transparência do glitch/invulnerabilidade ao final do frame
    self.aplicar_efeito_glitch()

  def animar(self, lista_frames):
    self.timer_piscada = 0
    self.index_frame += self.velocidade_animacao
    if self.index_frame >= len(lista_frames):
      self.index_frame = 0
    self.image = lista_frames[int(self.index_frame)]

  def animar_pulo(self):
    self.timer_piscada = 0
    frames = (
        self.frames_pulo
        if self.olhando_para == 'direita'
        else self.frames_pulo_esquerda
    )

    if self.velocidade_y <= 0:
      self.image = frames[0]
    else:
      self.image = frames[1]