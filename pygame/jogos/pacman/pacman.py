import pygame

COR_PACMAN = (255, 255, 0)

class Pacman:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna

    def posicao(self):
        return (self.linha, self.coluna)

    def desenhar_pacman(self, tela, tamanho_celula):
        centro_x = self.coluna * tamanho_celula + tamanho_celula // 2
        centro_y = self.linha * tamanho_celula + tamanho_celula // 2
        pygame.draw.circle(tela, COR_PACMAN, (centro_x, centro_y), tamanho_celula // 2 - 4)

    def colisao(self, linha, coluna, valor, labirinto):
        linhas = len(labirinto)
        colunas = len(labirinto[0])
        if 0 <= linha < linhas and 0 <= coluna < colunas:
            return labirinto[linha][coluna] == valor
        return True 

    def mover_pacman(self, direcao, labirinto):
        delta = {
            "cima": (-1, 0),
            "baixo": (1, 0),
            "esquerda": (0, -1),
            "direita": (0, 1),
        }
        d_linha, d_coluna = delta[direcao]
        nova_linha = self.linha + d_linha
        nova_coluna = self.coluna + d_coluna

        if not self.colisao(nova_linha, nova_coluna, 1, labirinto):
            self.linha = nova_linha
            self.coluna = nova_coluna