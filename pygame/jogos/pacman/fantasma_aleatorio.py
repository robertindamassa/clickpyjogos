import copy
import random
from time import sleep

from fantasma import Fantasma


class FantasmaAleatorio(Fantasma):

    def mover(self, pacman, labirinto):
        random.shuffle(self.direcao)

        self.contador_movimento += 1

        if self.contador_movimento >= self.intervalo_movimento:
            for d_linha, d_coluna in self.direcao:
                nova_linha, nova_coluna = self.linha + d_linha, self.coluna + d_coluna
                if not self.colisao(nova_linha, nova_coluna, labirinto):
                    self.linha, self.coluna = nova_linha, nova_coluna
                    self.contador_movimento = 0
                    break