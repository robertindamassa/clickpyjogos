import asyncio
import pygame

# inicializar
pygame.init()
pygame.mixer.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Breakout ClickPyJogos")

try:
    pygame.mixer.music.load("bitsong.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
except Exception as e:
    print("Aviso de áudio:", e)

tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(350, 750, tamanho_jogador, 15)
velocidade_jogador = 450

qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos

def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas + 40, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos

cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 150, 255),
    "verde": (0, 255, 0)
}

venceu = False
perdeu = False
movimento_bola = [5, -5]
blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

def desenhar_inicio_jogo():
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador, border_radius=4)
    pygame.draw.rect(tela, cores["branca"], bola, border_radius=7)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco, border_radius=2)

def desenhar_fim_de_jogo():
    if not (venceu or perdeu):
        return

    largura_caixa = 420
    altura_caixa = 130
    pos_x = (tamanho_tela[0] - largura_caixa) // 2
    pos_y = (tamanho_tela[1] - altura_caixa) // 2

    superficie = pygame.Surface((largura_caixa, altura_caixa))
    superficie.set_alpha(225)
    superficie.fill((15, 15, 25))
    tela.blit(superficie, (pos_x, pos_y))

    cor_borda = (0, 255, 0) if venceu else (255, 50, 50)
    pygame.draw.rect(tela, cor_borda, (pos_x, pos_y, largura_caixa, altura_caixa), 2, border_radius=8)

    fonte_titulo = pygame.font.Font(None, 48)
    fonte_sub = pygame.font.Font(None, 28)

    if venceu:
        texto_titulo = fonte_titulo.render("Parabéns!", True, (0, 255, 0))
        texto_sub = fonte_sub.render("Aperte R para reiniciar o jogo", True, (255, 255, 255))
    else:
        texto_titulo = fonte_titulo.render("Você perdeu!", True, (255, 50, 50))
        texto_sub = fonte_sub.render("Aperte R para reiniciar", True, (255, 255, 255))

    rect_titulo = texto_titulo.get_rect(center=(tamanho_tela[0] // 2, pos_y + 45))
    rect_sub = texto_sub.get_rect(center=(tamanho_tela[0] // 2, pos_y + 90))

    tela.blit(texto_titulo, rect_titulo)
    tela.blit(texto_sub, rect_sub)

def reiniciar_jogo():
    global blocos, movimento_bola, venceu, perdeu
    bola.x = 100
    bola.y = 500
    jogador.x = 350
    movimento_bola = [5, -5]
    blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)
    venceu = False
    perdeu = False

def movimentar_jogador(teclas, tempo_quadro):
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador.x += velocidade_jogador * tempo_quadro
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador.x -= velocidade_jogador * tempo_quadro

    # Suporte a mouse
    mouse_botoes = pygame.mouse.get_pressed()
    if mouse_botoes[0]:
        mouse_x = pygame.mouse.get_pos()[0]
        jogador.centerx = mouse_x

    jogador.x = max(0, min(jogador.x, tamanho_tela[0] - tamanho_jogador))

def movimentar_bola(bola):
    movimento = movimento_bola
    bola.x = bola.x + movimento[0]
    bola.y = bola.y + movimento[1]

    if bola.x <= 0:
        movimento[0] = -movimento[0]
    if bola.y <= 0:
        movimento[1] = -movimento[1]
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = -movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        movimento = None

    if movimento and jogador.colliderect(bola):
        movimento[1] = -abs(movimento[1])
    if movimento:
        for bloco in blocos:
            if bloco.colliderect(bola):
                blocos.remove(bloco)
                movimento[1] = -movimento[1]
                break
    return movimento

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarela"])
    tela.blit(texto, (10, 770))
    return pontuacao >= qtde_total_blocos

async def main():
    global venceu, perdeu, movimento_bola
    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        tempo_quadro = relogio.tick(60) / 1000
        if tempo_quadro > 0.1:
            tempo_quadro = 0.016

        desenhar_inicio_jogo()
        desenhar_blocos(blocos)
        if atualizar_pontuacao(qtde_total_blocos - len(blocos)):
            venceu = True

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                rodando = False
                break
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                if venceu or perdeu:
                    reiniciar_jogo()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if venceu or perdeu:
                    reiniciar_jogo()

        if not rodando:
            break

        if not (venceu or perdeu):
            teclas = pygame.key.get_pressed()
            movimentar_jogador(teclas, tempo_quadro)
            movimento_bola = movimentar_bola(bola)
            if not movimento_bola:
                perdeu = True

        desenhar_fim_de_jogo()
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
