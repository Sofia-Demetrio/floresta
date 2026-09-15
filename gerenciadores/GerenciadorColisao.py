import os
import pygame


class GerenciadorColisao:

  def __init__(
      self,
      player,
      grupo_moedas,
      grupo_monstros=None,
      pos_inicial_player=(50, 255),
  ):
    self.player = player
    self.grupo_moedas = grupo_moedas
    self.grupo_monstros = grupo_monstros
    self.pontos_moedas = 0

    # Vidas e posição inicial (spawn point)
    self.vidas_player = 3
    self.pos_inicial_player = pos_inicial_player

    # Diretório raiz
    diretorio_raiz = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )

    # Áudio - Som da Moeda
    caminho_som_moeda = os.path.join(
        diretorio_raiz, 'assets', 'som', 'coin-collision-sound.mp3'
    )
    self.som_moeda = None
    if os.path.exists(caminho_som_moeda):
      try:
        self.som_moeda = pygame.mixer.Sound(caminho_som_moeda)
        self.som_moeda.set_volume(0.5)
      except pygame.error as e:
        print(f'[ERRO SOM MOEDA] Não foi possível carregar o som: {e}')
    else:
      print(
          f'[ERRO CAMINHO] Som da moeda não encontrado em: {caminho_som_moeda}'
      )

    # Áudio - Som do Cogumelo Atingido
    caminho_som_cogumelo = os.path.join(
        diretorio_raiz, 'assets', 'som', 'gameboy-pluck.mp3'
    )
    self.som_cogumelo = None
    if os.path.exists(caminho_som_cogumelo):
      try:
        self.som_cogumelo = pygame.mixer.Sound(caminho_som_cogumelo)
        self.som_cogumelo.set_volume(0.6)
      except pygame.error as e:
        print(f'[ERRO SOM COGUMELO] Não foi possível carregar o som: {e}')
    else:
      print(
          '[ERRO CAMINHO] Som do cogumelo não encontrado em:'
          f' {caminho_som_cogumelo}'
      )

    # Áudio - Som de Dano do Player (Game Over / Dano)
    caminho_som_dano = os.path.join(
        diretorio_raiz, 'assets', 'som', 'game-over.mp3'
    )
    self.som_dano = None
    if os.path.exists(caminho_som_dano):
      try:
        self.som_dano = pygame.mixer.Sound(caminho_som_dano)
        self.som_dano.set_volume(0.6)
      except pygame.error as e:
        print(f'[ERRO SOM DANO] Não foi possível carregar o som: {e}')
    else:
      print(
          f'[ERRO CAMINHO] Som de dano não encontrado em: {caminho_som_dano}'
      )

  def checar_todas(self):
    self.checar_coleta_moedas()
    self.checar_colisao_monstros()

  def checar_coleta_moedas(self):
    moedas_coletadas = pygame.sprite.spritecollide(
        self.player, self.grupo_moedas, True
    )

    if moedas_coletadas:
      if self.som_moeda:
        self.som_moeda.play()

      self.pontos_moedas += len(moedas_coletadas)
      print(f'Moedas coletadas: {self.pontos_moedas}')

  def checar_colisao_monstros(self):
    if not self.grupo_monstros:
      return

    monstros_atingidos = pygame.sprite.spritecollide(
        self.player, self.grupo_monstros, False
    )

    for monstro in monstros_atingidos:
      margem_cabeca = monstro.rect.top + 20

      # Pulo na cabeça do monstro (jogador caindo)
      if (
          self.player.velocidade_y > 0
          and self.player.rect.bottom <= margem_cabeca
      ):
        if not getattr(monstro, 'atordoado', False):
          monstro.levar_dano()

          # Toca o som gameboy-pluck.mp3 ao atingir o cogumelo
          if self.som_cogumelo:
            self.som_cogumelo.play()

          print('Monstro atordoado!')

        # Impulso para cima ao pisar no monstro
        self.player.velocidade_y = -10

      # Colisão lateral/por baixo (dano no jogador)
      else:
        if not getattr(monstro, 'atordoado', False) and not getattr(
            self.player, 'invulneravel', False
        ):
          self.aplicar_dano_jogador()

  def aplicar_dano_jogador(self):
    if hasattr(self.player, 'levar_dano'):
      self.player.levar_dano()

    # Toca o som game-over.mp3 ao tomar dano
    if self.som_dano:
      self.som_dano.play()

    self.vidas_player -= 1
    print(f'Jogador recebeu dano! Vidas restantes: {self.vidas_player}')

    if self.vidas_player <= 0:
      self.reiniciar_jogador()

  def reiniciar_jogador(self):
    print('Vidas esgotadas! Voltando para a posição inicial do jogo...')
    self.vidas_player = 3

    # Reseta exatamente para a posição inicial de início da fase
    self.player.rect.x = self.pos_inicial_player[0]
    self.player.rect.y = self.pos_inicial_player[1]

    # Reseta física de pulo e colisão com chão
    self.player.velocidade_x = 0
    self.player.velocidade_y = 0
    self.player.no_chao = True
    self.player.chao_y = self.pos_inicial_player[1]

    # Remove qualquer efeito de invulnerabilidade/glitch pendente
    self.player.invulneravel = False
    self.player.tempo_invulneravel = 0
    self.player.image.set_alpha(255)