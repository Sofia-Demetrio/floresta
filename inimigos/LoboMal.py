import os
import pygame 

class lobo_mal(pygame.sprite.Sprite):
  
  def __init__(self, pos_x, pos_y, limite_esquerda=0, limite_direita=300, posicao_inicial=None, tamanho_padrao=None):
    super().__init__()

    diretorio_raiz = os.path.abspath(
      os.path.join(os.path.dirname(__file__), '..')
    )
    pasta_sprites = os.path.join(
      diretorio_raiz, 'assets', 'imagens', 'sprites', 'lobo_mal'
    )
    self.imagem_parada = pygame.image.load(
        os.path.join(pasta_sprites, 'lobo mal andando.png')
    ).convert_alpha()

    self.largura_padrao = self.imagem_parada.get_width()
    self.altura_padrao = self.imagem_parada.get_height()
    self.tamanho_padrao = (self.largura_padrao, self.altura_padrao)

#frames andando pra esquerda 
    self.frames_esquerda = [
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(pasta_sprites, f'lobo mal andando ({i}).png')
            ).convert_alpha(),
            self.tamanho_padrao,
        )
        for i in range(1, 4)
    ]
#frames andando pra direita
    self.frames_direita = [
        pygame.transform.flip(frame, True, False)
        for frame in self.frames_esquerda
    ]

#frames andando pra cima 
    self.frames_cima = [
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(pasta_sprites, f'lobo mal cima ({i}).png')
            ).convert_alpha(),
            self.tamanho_padrao,
        )
        for i in range(1, 4)
    ]

    # Estado inicial e Rect
    self.index_frame = 0
    self.image = self.imagem_parada
    self.rect = self.image.get_rect()

    self.pos_x_mundo = pos_x
    self.rect.x = pos_x
    self.rect.y = pos_y

    self.limite_esquerda = pos_x + limite_esquerda
    self.limite_direita = pos_x + limite_direita

    self.velocidade_animacao = 0.15
    self.velocidade_movimento = 2
    self.direcao = -1

    # --- CONTROLE DE STUN ---
    self.atordoado = False
    self.duracao_stun = 1000  # Tempo de stun em milissegundos (1 segundo)
    self.tempo_inicio_stun = 0

  def levar_dano(self):
    """Método acionado ao tomar um golpe do jogador ou colisão."""
    if not self.atordoado:
      self.atordoado = True
      self.tempo_inicio_stun = pygame.time.get_ticks()
      self.index_frame = 0  # Reinicia o ciclo de animação para o Stun

      if self.som_stun:
        self.som_stun.play()

  def update(self, cam_x=0):
    tempo_atual = pygame.time.get_ticks()

    # --- LÓGICA QUANDO ESTÁ ATORDOADO ---
    if self.atordoado:
      # O monstro NÃO anda enquanto estiver atordoado
      # Escolhe os frames de stun espelhados de acordo com a última direção
      frames_stun_atuais = (
          self.frames_stun_direita
          if self.direcao == 1
          else self.frames_stun_esquerda
      )
      self.animar(frames_stun_atuais)

      # Checa se o tempo de stun acabou
      if tempo_atual - self.tempo_inicio_stun >= self.duracao_stun:
        self.atordoado = False
        self.index_frame = 0  # Reseta o frame para voltar a andar

    # --- LÓGICA NORMAL (PATRULHA) ---
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

    # Atualiza a posição na tela com o deslocamento da câmera
    self.rect.x = self.pos_x_mundo + cam_x

  def animar(self, lista_frames):
    self.index_frame += self.velocidade_animacao
    if self.index_frame >= len(lista_frames):
      self.index_frame = 0
    self.image = lista_frames[int(self.index_frame)]