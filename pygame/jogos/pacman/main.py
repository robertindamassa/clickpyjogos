import asyncio
import sys
import pygame

from jogo import Jogo

COR_FUNDO = (0, 0, 0)
COR_PONTUACAO = (255, 255, 255)

LABIRINTO = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

LINHAS = len(LABIRINTO)
COLUNAS = len(LABIRINTO[0])

TAMANHO_CELULA = 40
LARGURA_TELA = COLUNAS * TAMANHO_CELULA
ALTURA_TELA = LINHAS * TAMANHO_CELULA
pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load("pacmantheme.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
except Exception as e:
    print("Aviso de áudio:", e)

async def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Pac-Man ClickPyJogos")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 28)

    jogo = Jogo(LABIRINTO)
    rodando = True

    if not jogo.labirinto:
        print("LABIRINTO INVALIDO")
        return

    while rodando:
        rodando = jogo.evento()

        jogo.atualizar()

        tela.fill(COR_FUNDO)
        jogo.desenhar_labirinto(tela, TAMANHO_CELULA)
        jogo.desenhar_pellets(tela, TAMANHO_CELULA)
        jogo.pacman.desenhar_pacman(tela, TAMANHO_CELULA)
        for fantasma in jogo.fantasmas:
            fantasma.desenhar(tela, TAMANHO_CELULA)

        texto = fonte.render(f"Pontos: {jogo.pontuacao:04d}   Vidas: {jogo.vida}    Recorde: {jogo.recorde}", True, COR_PONTUACAO)
        tela.blit(texto, (10, ALTURA_TELA - 30))

        jogo.desenhar_fim_de_jogo(tela, LARGURA_TELA, ALTURA_TELA)

        pygame.display.flip()
        fps = jogo.frame if jogo.frame > 0 else 60
        relogio.tick(fps)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())