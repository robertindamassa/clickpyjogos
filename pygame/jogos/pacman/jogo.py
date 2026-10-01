import json

import pygame

from excecoes import SemVidasError
from fantasma_aleatorio import FantasmaAleatorio
from fantasma_perseguidor import FantasmaPerseguidor
from pacman import Pacman

COR_PAREDE = (33, 33, 222)
COR_PONTO = (255, 255, 255)
COR_FANTASMA_ALEATORIO = (255, 0, 0)
COR_FANTASMA_PERSEGUIDOR = (255, 105, 180)
COR_FANTASMA_CIANO = (0, 255, 255)
COR_TEXTO_VITORIA = (0, 255, 0)
COR_TEXTO_DERROTA = (255, 50, 50)
COR_TEXTO_SUB = (255, 255, 255)

TAMANHO_PONTO = 4
PONTOS_POR_PELLET = 10
VIDAS_INICIAIS = 3

ARQUIVO_RECORDE = "recorde.json"

class Jogo:
    def __init__(self, labirinto) -> None:
        self.labirinto = self.validar_labirinto(labirinto)
        self.frame = 60
        self.recorde = self.carregar_recorde()
        
        
        if not pygame.font.get_init():
            pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont(None, 34)
        self.fonte_sub = pygame.font.SysFont(None, 22)

        
        self.pacman = None
        self.pellets = set()
        self._pontuacao = 0
        self.vida = VIDAS_INICIAIS
        self.fantasmas = []
        
        self.reiniciar()

    def reiniciar(self):
        self.pacman = Pacman(1, 1)
        self.pellets = self.criar_pellets()
        self._pontuacao = 0
        self.vida = VIDAS_INICIAIS
        self.recorde = self.carregar_recorde()
        self.frame = 60
        self.fantasmas = [
            FantasmaAleatorio(5, 8, COR_FANTASMA_ALEATORIO),
            FantasmaPerseguidor(1, 8, COR_FANTASMA_PERSEGUIDOR),
            FantasmaPerseguidor(9, 8, COR_FANTASMA_CIANO),
        ]

    @property
    def pontuacao(self):
        return self._pontuacao

    def criar_pellets(self):
        posicao_inicial_pacman = self.pacman.posicao() if self.pacman else (1, 1)
        pellets = {
            (linha, coluna)
            for linha in range(len(self.labirinto))
            for coluna in range(len(self.labirinto[0]))
            if self.labirinto[linha][coluna] == 0 and (linha, coluna) != posicao_inicial_pacman
        }
        return pellets

    def desenhar_pellets(self, tela, tamanho_celula):
        for linha, coluna in self.pellets:
            centro_x = coluna * tamanho_celula + tamanho_celula // 2
            centro_y = linha * tamanho_celula + tamanho_celula // 2
            pygame.draw.circle(tela, COR_PONTO, (centro_x, centro_y), TAMANHO_PONTO)

    def atualizar(self):
        if self.venceu() or self.perdeu():
            return

        posicao_atual = self.pacman.posicao()
        if posicao_atual in self.pellets:
            self.pellets.remove(posicao_atual)
            self._pontuacao += PONTOS_POR_PELLET
            if self.venceu():
                if self.pontuacao > self.recorde:
                    self.salvar_recorde()

        for fantasma in self.fantasmas:
            fantasma.mover(self.pacman, self.labirinto)
            if fantasma.posicao() == self.pacman.posicao():
                self.perder_vida()
                break  

    def perder_vida(self):
        self.vida -= 1
        self.pacman.linha, self.pacman.coluna = 1, 1
         
        # Reposicionando os fantasmas no lugar após perder vida
        self.fantasmas[0].linha, self.fantasmas[0].coluna = 5, 8
        self.fantasmas[1].linha, self.fantasmas[1].coluna = 1, 8
        self.fantasmas[2].linha, self.fantasmas[2].coluna = 9, 8
        if self.vida <= 0:
            self.vida = 0
            if self.pontuacao > self.recorde:
                self.salvar_recorde()

    def validar_labirinto(self, labirinto):
        tamanho_coluna = len(labirinto[0])

        for linha in labirinto:
            if len(linha) != tamanho_coluna:
                return []

        return labirinto

    def desenhar_labirinto(self, tela, tamanho_celula):
        linhas = len(self.labirinto)
        colunas = len(self.labirinto[0])

        for linha in range(linhas):
            for coluna in range(colunas):
                if self.labirinto[linha][coluna] == 1:
                    retangulo = pygame.Rect(
                        coluna * tamanho_celula,
                        linha * tamanho_celula,
                        tamanho_celula,
                        tamanho_celula,
                    )
                    pygame.draw.rect(tela, COR_PAREDE, retangulo)

    def desenhar_fim_de_jogo(self, tela, largura_tela, altura_tela):
        if not (self.venceu() or self.perdeu()):
            return

        largura_caixa = 320
        altura_caixa = 100
        pos_x = (largura_tela - largura_caixa) // 2
        pos_y = (altura_tela - altura_caixa) // 2

        # texto
        superficie = pygame.Surface((largura_caixa, altura_caixa))
        superficie.set_alpha(225)
        superficie.fill((15, 15, 25))
        tela.blit(superficie, (pos_x, pos_y))

        
        cor_borda = COR_TEXTO_VITORIA if self.venceu() else COR_TEXTO_DERROTA
        pygame.draw.rect(tela, cor_borda, (pos_x, pos_y, largura_caixa, altura_caixa), 2, border_radius=8)

        if self.venceu():
            texto_titulo = self.fonte_titulo.render("Parabéns!", True, COR_TEXTO_VITORIA)
            texto_sub = self.fonte_sub.render("Aperte R para reiniciar o jogo", True, COR_TEXTO_SUB)
        else:
            texto_titulo = self.fonte_titulo.render("Você perdeu!", True, COR_TEXTO_DERROTA)
            texto_sub = self.fonte_sub.render("Aperte R para reiniciar", True, COR_TEXTO_SUB)

        rect_titulo = texto_titulo.get_rect(center=(largura_tela // 2, pos_y + 35))
        rect_sub = texto_sub.get_rect(center=(largura_tela // 2, pos_y + 70))

        tela.blit(texto_titulo, rect_titulo)
        tela.blit(texto_sub, rect_sub)

    def evento(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    if self.venceu() or self.perdeu():
                        self.reiniciar()
                elif not (self.venceu() or self.perdeu()):
                    if evento.key == pygame.K_LEFT:
                        self.pacman.mover_pacman("esquerda", self.labirinto)
                    elif evento.key == pygame.K_RIGHT:
                        self.pacman.mover_pacman("direita", self.labirinto)
                    elif evento.key == pygame.K_UP:
                        self.pacman.mover_pacman("cima", self.labirinto)
                    elif evento.key == pygame.K_DOWN:
                        self.pacman.mover_pacman("baixo", self.labirinto)
                    elif evento.key == pygame.K_SPACE:
                        if self.frame == 60:
                            self.frame = 0
                        else:
                            self.frame = 60

        return True

    def salvar_recorde(self):
        self.recorde = self.pontuacao
        with open(ARQUIVO_RECORDE, "w", encoding="utf-8") as arquivo:
            json.dump({
                "recorde": self.pontuacao
            },
            arquivo)

    def carregar_recorde(self):
        try:
            with open(ARQUIVO_RECORDE, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados.get("recorde", 0)
        except FileNotFoundError:
            return 0

    def venceu(self):
        return len(self.pellets) == 0

    def perdeu(self):
        return self.vida <= 0

    