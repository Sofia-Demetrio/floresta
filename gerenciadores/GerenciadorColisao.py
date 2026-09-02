import pygame

class GerenciadorColisao:
    def __init__(self, player, grupo_moedas):
        self.player = player
        self.grupo_moedas = grupo_moedas
        self.pontos_moedas = 0

    def checar_todas(self):
        self.checar_coleta_moedas()
        # Aqui você poderá adicionar futuras checagens:
        # self.checar_inimigos()
        # self.checar_plataformas()

    def checar_coleta_moedas(self):
        # Detecta a colisão e remove a moeda do grupo (dokill=True)
        moedas_coletadas = pygame.sprite.spritecollide(self.player, self.grupo_moedas, True)
        
        if moedas_coletadas:
            self.pontos_moedas += len(moedas_coletadas)
            print(f"Moedas coletadas: {self.pontos_moedas}")