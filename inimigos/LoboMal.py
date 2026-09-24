import os
import pygame


class LoboMal(pygame.sprite.Sprite):

  def __init__(self, pos_x, pos_y, limite_esquerda=0, limite_direita=300):
    super().__init__()

    diretorio_raiz = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
    pasta_sprites = os.path.join(
        diretorio_raiz, 'assets', 'imagens', 'sprites', 'inimigo'
    )

    # Base principal
    caminho_base = os.path.join(pasta_sprites, 'lobo mal andando.png')
    if os.path.exists(caminho_base):
      self.image_parada = pygame.image.load(caminho_base).convert_alpha()
    else:
      self.image_parada = pygame.Surface((48, 48))
      self.image_parada.fill((100, 100, 100))

    self.largura_padrao = 100
    self.altura_padrao = 300
    self.tamanho_padrao = (self.largura_padrao, self.altura_padrao)

    # Função auxiliar para carregar frames com fallback automático
    def carregar_frames(prefixo):
      frames = []
      for i in range(1, 4):
        caminho = os.path.join(pasta_sprites, f'{prefixo} {i}.png')
        if os.path.exists(caminho):
          img = pygame.image.load(caminho).convert_alpha()
          frames.append(pygame.transform.scale(img, self.tamanho_padrao))
        else:
          # Tenta sem o número se não achar o número
          caminho_alt = os.path.join(pasta_sprites, f'{prefixo}.png')
          if os.path.exists(caminho_alt):
            img = pygame.image.load(caminho_alt).convert_alpha()
            frames.append(pygame.transform.scale(img, self.tamanho_padrao))
          else:
            frames.append(self.image_parada)
      return frames

    self.frames_esquerda = carregar_frames('lobo mal andando')
    self.frames_direita = [
        pygame.transform.flip(f, True, False) for f in self.frames_esquerda
    ]
    self.frames_frente = carregar_frames('lobo mal frente')
    self.frames_costas = carregar_frames('lobo mal costas')

    self.frames_stun_esquerda = self.frames_esquerda
    self.frames_stun_direita = self.frames_direita

    self.index_frame = 0
    self.image = self.image_parada
    self.rect = self.image.get_rect()

    self.pos_x_mundo = pos_x
    self.rect.x = pos_x
    self.rect.y = pos_y

    self.limite_esquerda = pos_x + limite_esquerda
    self.limite_direita = pos_x + limite_direita

    self.velocidade_animacao = 0.15
    self.velocidade_movimento = 2
    self.direcao = -1

    self.atordoado = False
    self.duracao_stun = 1000
    self.tempo_inicio_stun = 0

  def levar_dano(self):
    if not self.atordoado:
      self.atordoado = True
      self.tempo_inicio_stun = pygame.time.get_ticks()
      self.index_frame = 0

  def update(self, cam_x=0):
    tempo_atual = pygame.time.get_ticks()

    if self.atordoado:
      frames_stun = (
          self.frames_stun_direita
          if self.direcao == 1
          else self.frames_stun_esquerda
      )
      self.animar(frames_stun)
      if tempo_atual - self.tempo_inicio_stun >= self.duracao_stun:
        self.atordoado = False
        self.index_frame = 0
    else:
      self.pos_x_mundo += self.velocidade_movimento * self.direcao
      if self.pos_x_mundo >= self.limite_direita:
        self.pos_x_mundo = self.limite_direita
        self.direcao = -1
      elif self.pos_x_mundo <= self.limite_esquerda:
        self.pos_x_mundo = self.limite_esquerda
        self.direcao = 1

      if self.direcao == 1:
        self.animar(self.frames_direita)
      else:
        self.animar(self.frames_esquerda)

    self.rect.x = self.pos_x_mundo + cam_x

  def animar(self, lista_frames):
    self.index_frame += self.velocidade_animacao
    if self.index_frame >= len(lista_frames):
      self.index_frame = 0
    self.image = lista_frames[int(self.index_frame)]