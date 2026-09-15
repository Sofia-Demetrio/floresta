import os
import pygame

from gerenciadores.GerenciadorColisao import GerenciadorColisao
from inimigos.Monstro import Monstro
from itens.Moeda import Moeda
from jogador.Player import Player


class Fase1:

  def __init__(self, diretorio_raiz, largura_virtual=736, altura_virtual=460):
    self.diretorio_raiz = diretorio_raiz
    self.LARGURA_VIRTUAL = largura_virtual
    self.ALTURA_VIRTUAL = altura_virtual

    # --- LIMITES VERTICAIS DO JOGADOR NA FASE ---
    self.LIMITE_Y_MIN = 250  # Posição Y máxima para SUBIR (evita flutuar no céu)
    self.LIMITE_Y_MAX = 330  # Posição Y máxima para DESCER (limite do chão)

    # Lista de caminhos possíveis para encontrar a imagem do fundo
    caminhos_fundo = [
        os.path.join(
            self.diretorio_raiz,
            'assets',
            'imagens',
            'sprites',
            'cenario',
            'floresta.jpg',
        ),
        os.path.join(
            self.diretorio_raiz, 'assets', 'imagens', 'cenario', 'floresta.jpg'
        ),
        os.path.join(
            self.diretorio_raiz, 'assets', 'imagens', 'floresta.jpg'
        ),
    ]

    caminho_fundo_valido = None
    for caminho in caminhos_fundo:
      if os.path.exists(caminho):
        caminho_fundo_valido = caminho
        break

    if caminho_fundo_valido:
      self.fundo = pygame.image.load(caminho_fundo_valido).convert()
    else:
      print('[AVISO] Imagem floresta.jpg não encontrada. Usando fundo padrão.')
      self.fundo = pygame.Surface(
          (self.LARGURA_VIRTUAL, self.ALTURA_VIRTUAL)
      )
      self.fundo.fill((34, 139, 34))

    self.LARGURA_FUNDO = self.fundo.get_width()

    # --- HUD ---
    self.fonte_hud = pygame.font.SysFont('Arial', 20, bold=True)

    caminho_moeda_4 = os.path.join(
        self.diretorio_raiz,
        'assets',
        'imagens',
        'sprites',
        'itens',
        'moeda 4.png',
    )
    if not os.path.exists(caminho_moeda_4):
      caminho_moeda_4 = os.path.join(
          self.diretorio_raiz, 'assets', 'imagens', 'moeda 4.png'
      )

    if os.path.exists(caminho_moeda_4):
      moeda_hud_original = pygame.image.load(caminho_moeda_4).convert_alpha()
      self.moeda_hud_img = pygame.transform.scale(moeda_hud_original, (24, 24))
    else:
      self.moeda_hud_img = pygame.Surface((24, 24))
      self.moeda_hud_img.fill((255, 215, 0))

    # --- MÚSICA ---
    caminho_musica = os.path.join(
        self.diretorio_raiz,
        'assets',
        'som',
        'paulyudin-fairy-tale-ballet-310250.mp3',
    )
    if os.path.exists(caminho_musica):
      try:
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        print('Música carregada e tocando em loop!')
      except pygame.error as e:
        print(f'[ERRO PYGAME] Falha ao reproduzir áudio: {e}')
    else:
      print(f'[ERRO CAMINHO] Música não encontrada em:\n{caminho_musica}')

    # --- ENTIDADES DO NÍVEL ---
    self.pos_inicial_player = (50, 255)
    self.player = Player(self.pos_inicial_player[0], self.pos_inicial_player[1])

    self.moedas = pygame.sprite.Group()
    self.moedas.add(Moeda(300, 320))
    self.moedas.add(Moeda(600, 200))
    self.moedas.add(Moeda(900, 320))
    self.moedas.add(Moeda(1200, 200))
    self.moedas.add(Moeda(1500, 320))

    self.monstros = pygame.sprite.Group()
    self.monstros.add(
        Monstro(500, 320, limite_esquerda=-100, limite_direita=200)
    )
    self.monstros.add(
        Monstro(1000, 320, limite_esquerda=-150, limite_direita=150)
    )

    self.gerenciador_colisao = GerenciadorColisao(
        player=self.player,
        grupo_moedas=self.moedas,
        grupo_monstros=self.monstros,
        pos_inicial_player=self.pos_inicial_player,
    )
    self.cam_x = 0

  def atualizar(self):
    self.player.update()

    # --- RESTRIÇÃO DO MOVIMENTO VERTICAL DO JOGADOR ---
    # Só limita no Y quando o jogador estiver no chão (para permitir a física do pulo)
    if getattr(self.player, 'no_chao', True):
      if self.player.rect.y < self.LIMITE_Y_MIN:
        self.player.rect.y = self.LIMITE_Y_MIN
        if hasattr(self.player, 'chao_y'):
          self.player.chao_y = self.LIMITE_Y_MIN

      elif self.player.rect.y > self.LIMITE_Y_MAX:
        self.player.rect.y = self.LIMITE_Y_MAX
        if hasattr(self.player, 'chao_y'):
          self.player.chao_y = self.LIMITE_Y_MAX

    # --- CÂMERA ADAPTATIVA (HORIZONTAL) ---
    if (
        self.player.rect.right > self.LARGURA_VIRTUAL - 150
        and self.player.velocidade_x > 0
    ):
      self.cam_x -= self.player.velocidade_x
      self.player.rect.right = self.LARGURA_VIRTUAL - 150
    elif self.player.rect.left < 150 and self.player.velocidade_x < 0:
      self.cam_x -= self.player.velocidade_x
      self.player.rect.left = 150

    self.moedas.update(self.cam_x)
    self.monstros.update(self.cam_x)
    self.gerenciador_colisao.checar_todas()

    # Reseta câmera se o jogador renascer após perder todas as vidas
    if (
        self.gerenciador_colisao.vidas_player == 3
        and self.player.rect.x == self.pos_inicial_player[0]
    ):
      self.cam_x = 0

  def desenhar(self, superficie_virtual):
    # Parallax do fundo
    offset_fundo = self.cam_x % self.LARGURA_FUNDO
    superficie_virtual.blit(
        self.fundo, (offset_fundo - self.LARGURA_FUNDO, 0)
    )
    superficie_virtual.blit(self.fundo, (offset_fundo, 0))

    # Entidades
    self.moedas.draw(superficie_virtual)
    self.monstros.draw(superficie_virtual)
    superficie_virtual.blit(self.player.image, self.player.rect)

    # HUD - Moedas
    superficie_virtual.blit(self.moeda_hud_img, (15, 15))

    texto_moedas = self.fonte_hud.render(
        f'x {self.gerenciador_colisao.pontos_moedas}', True, (255, 255, 255)
    )
    sombra_moedas = self.fonte_hud.render(
        f'x {self.gerenciador_colisao.pontos_moedas}', True, (0, 0, 0)
    )

    pos_x_texto = 15 + self.moeda_hud_img.get_width() + 8
    pos_y_texto = (
        15
        + (self.moeda_hud_img.get_height() // 2)
        - (texto_moedas.get_height() // 2)
    )

    superficie_virtual.blit(sombra_moedas, (pos_x_texto + 1, pos_y_texto + 1))
    superficie_virtual.blit(texto_moedas, (pos_x_texto, pos_y_texto))