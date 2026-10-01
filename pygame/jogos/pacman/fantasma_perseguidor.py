from time import sleep
import random

from fantasma import Fantasma


class FantasmaPerseguidor(Fantasma):

    def mover(self, pacman, labirinto):
        melhor_direcao = None
        menor_distancia = None

        self.contador_movimento += 1

        if self.contador_movimento >= self.intervalo_movimento:

            distancia_pacman = abs(self.linha - pacman.linha) + abs(self.coluna - pacman.coluna)

            if distancia_pacman > 4:
                random.shuffle(self.direcao)

                for d_linha, d_coluna in self.direcao:
                    nova_linha = self.linha + d_linha
                    nova_coluna = self.coluna + d_coluna

                    if not self.colisao(nova_linha, nova_coluna, labirinto):
                        self.linha = nova_linha
                        self.coluna = nova_coluna
                        self.contador_movimento = 0
                        return

            for d_linha, d_coluna in self.direcao:
                nova_linha, nova_coluna = self.linha + d_linha, self.coluna + d_coluna

                if self.colisao(nova_linha, nova_coluna, labirinto):
                    continue

                distancia = abs(nova_linha - pacman.linha) + abs(nova_coluna - pacman.coluna)

                if menor_distancia is None or distancia < menor_distancia:
                    menor_distancia = distancia
                    melhor_direcao = (nova_linha, nova_coluna)

            if melhor_direcao:
                self.linha, self.coluna = melhor_direcao

            self.contador_movimento = 0