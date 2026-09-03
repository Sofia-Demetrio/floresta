import os
import pygame


class GerenciadorColisao:

  def __init__(self, player, grupo_moedas, grupo_monstros=None):
    self.player = player
    self.grupo_moedas = grupo_moedas
    self.grupo_monstros = grupo_monstros
    self.pontos_moedas = 0

    diretorio_raiz = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
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

    # Detecta monstros tocando no jogador (dokill=False para o monstro não sumir)
    monstros_atingidos = pygame.sprite.spritecollide(
        self.player, self.grupo_monstros, False
    )

    for monstro in monstros_atingidos:
      # Chama o método de stun do monstro se ele ainda não estiver atordoado
      if not monstro.atordoado:
        monstro.levar_dano()

        # Opcional: Se a sua classe Player tiver método para levar dano
        if hasattr(self.player, 'levar_dano'):
          self.player.levar_dano()