import pygame

class Fantasma:

    def __init__(self, linha, coluna, cor) -> None:
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
        self.direcao = [(-1, 0),(1, 0),(0, 1),(0, -1)]
        self.contador_movimento = 0
        self.intervalo_movimento = 20

    def posicao(self):
        return (self.linha, self.coluna)

    def mover(self, pacman, labirinto):
        raise NotImplementedError("Subclasse deve implementar mover()")

    def colisao(self, linha, coluna, labirinto):
        linhas = len(labirinto)
        colunas = len(labirinto[0])
        if 0 <= linha < linhas and 0 <= coluna < colunas:
            return labirinto[linha][coluna] == 1
        return True 

    def desenhar(self, tela, tamanho_celula):
        cx = self.coluna * tamanho_celula + tamanho_celula // 2
        cy = self.linha * tamanho_celula + tamanho_celula // 2
        pygame.draw.circle(tela, self.cor, (cx,cy), tamanho_celula // 2 - 4)