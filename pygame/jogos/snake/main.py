import asyncio
import json
import pygame
import random

pygame.init()
pygame.mixer.init()
try:
    pygame.mixer.music.load("snakey.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
except Exception as e:
    print("Aviso de áudio:", e)

pygame.display.set_caption("Jogo Snake Python")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
imagemdefund = pygame.image.load("fundopy.png")
imagem_fundo = pygame.transform.scale(imagemdefund, (largura, altura))

relogio = pygame.time.Clock()
fonte_titulo = pygame.font.SysFont(None, 34)
fonte_sub = pygame.font.SysFont(None, 22)
arquivo_recorde = "recorde.json"

# cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# parametros da cobrinha
tamanho_quadrado = 20
velocidade_jogo = 15

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelha, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])

def desenhar_fim_jogo(recorde):
    largura_caixa = 420
    altura_caixa = 150
    pos_x = (largura - largura_caixa) // 2
    pos_y = (altura - altura_caixa) // 2

    superficie = pygame.Surface((largura_caixa, altura_caixa))
    superficie.set_alpha(225)
    superficie.fill((15, 15, 25))
    tela.blit(superficie, (pos_x, pos_y))

    cor_borda = (255, 50, 50)
    pygame.draw.rect(tela, cor_borda, (pos_x, pos_y, largura_caixa, altura_caixa), 2, border_radius=8)

    texto_titulo = fonte_titulo.render("Você perdeu!", True, cor_borda)
    texto_recorde = fonte_sub.render(f"Seu recorde é: {recorde}", True, branca)
    texto_sub = fonte_sub.render("Aperte R para reiniciar", True, branca)

    rect_titulo = texto_titulo.get_rect(center=(largura // 2, pos_y + 35))
    rect_recorde = texto_recorde.get_rect(center=(largura // 2, pos_y + 75))
    rect_sub = texto_sub.get_rect(center=(largura // 2, pos_y + 115))

    tela.blit(texto_titulo, rect_titulo)
    tela.blit(texto_recorde, rect_recorde)
    tela.blit(texto_sub, rect_sub)

def carregar_recorde():
    try:
        with open(arquivo_recorde, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados.get("recorde", 0)
    except Exception:
        return 0

def salvar_recorde(recorde):
    try:
        with open(arquivo_recorde, "w", encoding="utf-8") as arquivo:
            json.dump({"recorde": recorde}, arquivo)
    except Exception:
        pass

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    if tecla == pygame.K_DOWN and velocidade_y != -tamanho_quadrado:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP and velocidade_y != tamanho_quadrado:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and velocidade_x != -tamanho_quadrado:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT and velocidade_x != tamanho_quadrado:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

async def main():
    recorde = carregar_recorde()
    rodando = True

    while rodando:
        fim_jogo = False
        x = largura / 2
        y = altura / 2
        velocidade_x = 0
        velocidade_y = 0
        tamanho_cobra = 1
        pixels = []
        comida_x, comida_y = gerar_comida()

        while rodando and not fim_jogo:
            tela.blit(imagemdefund, (0, 0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    break
                elif evento.type == pygame.KEYDOWN:
                    velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

            if not rodando:
                break

            desenhar_comida(tamanho_quadrado, comida_x, comida_y)

            x += velocidade_x
            y += velocidade_y

            pixels.append([x, y])
            if len(pixels) > tamanho_cobra:
                del pixels[0]

            if x < 0 or x >= largura or y < 0 or y >= altura:
                fim_jogo = True

            for pixel in pixels[:-1]:
                if pixel == [x, y]:
                    fim_jogo = True

            pontuacao = tamanho_cobra - 1
            if fim_jogo and pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)

            if not fim_jogo and x == comida_x and y == comida_y:
                tamanho_cobra += 1
                comida_x, comida_y = gerar_comida()

            desenhar_cobra(tamanho_quadrado, pixels)
            desenhar_pontuacao(pontuacao)
            pygame.display.update()
            relogio.tick(velocidade_jogo)
            await asyncio.sleep(0)

        while rodando and fim_jogo:
            tela.blit(imagemdefund, (0, 0))
            desenhar_fim_jogo(recorde)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    fim_jogo = False

            relogio.tick(velocidade_jogo)
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())