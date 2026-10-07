from django.shortcuts import render, Http404

# Dicionário com os jogos disponíveis no site
JOGOS = {
    'dinossauro': {
        'slug': 'dinossauro',
        'nome': 'Dinossauro',
        'titulo': 'Dinossauro T-Rex',
        'imagem': 'paginas/imagens/jogo_dinossauro.jpg',
        'controles': 'ESPAÇO ou SETA PARA CIMA: Pular | SETA PARA BAIXO: Abaixar | MOUSE: Iniciar / Reiniciar',
    },
    'flappybird': {
        'slug': 'flappybird',
        'nome': 'Flappy Bird',
        'titulo': 'Flappy Bird',
        'imagem': 'paginas/imagens/jogo_flappy.jpg',
        'controles': 'ESPAÇO, ENTER ou CLIQUE DO MOUSE: Voar / Bater Asas | R: Reiniciar o jogo',
    },
    'pacman': {
        'slug': 'pacman',
        'nome': 'Pac-Man',
        'titulo': 'Pac-Man',
        'imagem': 'paginas/imagens/jogo_pacman.jpg',
        'controles': 'SETAS DIRECIONAIS: Movimentar o Pac-Man | TECLA R: Reiniciar o jogo | ESPAÇO: Pausar',
    },
    'snake': {
        'slug': 'snake',
        'nome': 'Snake',
        'titulo': 'Snake (Cobrinha)',
        'imagem': 'paginas/imagens/jogo_snake.jpg',
        'controles': 'SETAS DIRECIONAIS: Mudar a direção da cobra | TECLA R: Reiniciar o jogo',
    },
    'breakout': {
        'slug': 'breakout',
        'nome': 'Breakout',
        'titulo': 'Breakout (Brick Breaker)',
        'imagem': 'paginas/imagens/jogo_breakout.jpg',
        'controles': 'SETAS ESQUERDA / DIREITA (ou teclas A / D ou MOUSE): Mover a barra | TECLA R ou CLIQUE: Reiniciar',
    },
}

# Página inicial que lista os jogos
def inicio(request):
    return render(request, "paginas/inicio.html", {"jogos": JOGOS})

# Página para jogar o jogo selecionado
def jogar(request, jogo):
    jogo_info = JOGOS.get(jogo)
    if not jogo_info:
        raise Http404("Jogo não encontrado")
    return render(request, "paginas/jogar.html", {"jogo": jogo_info})