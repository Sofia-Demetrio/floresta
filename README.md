# Floresta Encantada

O **Floresta Encantada** é um jogo de plataforma 2D desenvolvido em Python utilizando a biblioteca Pygame. O jogador explora um bosque mágico, coleta itens, enfrenta inimigos e avança pelas fases do jogo.

## Funcionalidades

* Movimentação do personagem para os lados e sistema de pulo.
* Física de gravidade e colisão com o cenário.
* Sistema de combate com arremesso de pedras.
* Inimigos como cogumelos, slimes e lobos.
* Coleta de moedas, morangos e melancias.
* Blocos de interrogação que podem fornecer vidas extras.
* Sistema de dano com período temporário de invulnerabilidade.
* Efeito de knockback ao receber dano.
* HUD para exibição das moedas e informações do jogo.
* Sistema de áudio com músicas e efeitos sonoros.
* Suporte a diferentes resoluções de tela.

## Controles

| Ação                  | Tecla      |
| --------------------- | ---------- |
| Mover para a esquerda | `A` ou `←` |
| Mover para a direita  | `D` ou `→` |
| Pular                 | `Espaço`   |
|                       |            |

## Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Biblioteca:** Pygame 2.6.1
* **Pixel Art:** Aseprite

## Como Executar

### Pré-requisitos

É necessário ter o Python 3.12 ou superior instalado.

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Sofia-Demetrio/floresta.git
cd floresta
```

2. Crie um ambiente virtual:

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale o Pygame:

```bash
pip install pygame
```

4. Execute o jogo:

```bash
python main.py
```
