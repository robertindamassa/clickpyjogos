import asyncio
import sys
import time
import pygame as pg 
from bird import Bird
from pipe import Pipe
from pygame import mixer 

pg.init()
mixer.init()

class Game:
    def __init__(self):
        # setting the window configurations
        self.width = 600 
        self.height = 768 
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Flappy Bird ClickPyJogos")
        self.clock = pg.time.Clock()
        self.move_speed = 200
        
        # Sfx
        try:
            self.flap_sound = mixer.Sound("assets/sfx/flap.wav")
            self.score_sound = mixer.Sound("assets/sfx/score.wav")
        except Exception:
            class DummySound:
                def play(self): pass
            self.flap_sound = DummySound()
            self.score_sound = DummySound()
        
        # Game Loop
        self.is_enter_pressed = False
        self.is_game_started = True
        
        # Bird  
        self.bird = Bird(self.scale_factor)

        self.font = pg.font.Font("assets/font.ttf", 24)
        
        self.start_text = self.font.render("Pressione ESPAÇO ou ENTER", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center=(300, 300))
        
        self.score_text = self.font.render("Score: 0 ", True, (255, 255, 255))
        self.score_text_rect = self.score_text.get_rect(center=(100, 30))
        
        self.restart_text = self.font.render("Clique ou Aperte R para Reiniciar", True, (255, 255, 255))
        self.restart_text_rect = self.restart_text.get_rect(center=(300, 300))
        
        # Score
        self.start_monitoring = False       
        self.score = 0 
        
        # Pipes
        self.pipes = []
        self.pipe_generate_counter = 105
      
        self.setupBgAndGround()
    
    async def gameLoop(self):
        last_time = time.time()
        rodando = True
        while rodando:
            # Calculating Delta Time
            new_time = time.time()
            dt = new_time - last_time 
            last_time = new_time
            if dt > 0.1:
                dt = 0.016

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    rodando = False
                    break
            
                if event.type == pg.KEYDOWN:
                    if not self.is_enter_pressed and (event.key in (pg.K_RETURN, pg.K_SPACE, pg.K_UP)):
                        self.is_enter_pressed = True
                        self.bird.is_not_collided = True
                        self.flap_sound.play()
                        self.bird.flap(dt)
                    elif self.is_enter_pressed and (event.key in (pg.K_SPACE, pg.K_UP)):
                        self.flap_sound.play()
                        self.bird.flap(dt)
                    elif not self.is_game_started and event.key in (pg.K_r, pg.K_RETURN, pg.K_SPACE):
                        self.restartGame()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if not self.is_enter_pressed:
                        self.is_enter_pressed = True
                        self.bird.is_not_collided = True
                        self.flap_sound.play()
                        self.bird.flap(dt)
                    elif self.is_enter_pressed:
                        self.flap_sound.play()
                        self.bird.flap(dt)
                    elif not self.is_game_started:
                        self.restartGame()
                        
            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)

        pg.quit()

    def checkScore(self):
        if len(self.pipes) > 0:
            first_pipe = self.pipes[0].rect_down
            bird_left = self.bird.rect.left
            bird_right = self.bird.rect.right

            if (bird_left > first_pipe.left and bird_right < first_pipe.right and not self.start_monitoring):
                self.start_monitoring = True
            
            if bird_left > first_pipe.right and self.start_monitoring:
                self.start_monitoring = False
                self.score += 1
                self.score_sound.play()
                self.score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
               
    def checkCollisions(self):
        pipe_collision = False
        
        if len(self.pipes):
            pipe_collision = self.bird.rect.colliderect(self.pipes[0].rect_down) or self.bird.rect.colliderect(self.pipes[0].rect_up)
        
        if pipe_collision:
            self.is_enter_pressed = False
            self.is_game_started = False
            
        if self.bird.rect.bottom > 568:
            self.bird.is_not_collided = False
            self.is_game_started = False
        
    def updateEverything(self, dt):
        if self.is_enter_pressed:
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right <= 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right <= 0:
                self.ground2_rect.x = self.ground1_rect.right 

            if self.pipe_generate_counter > 105:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
            self.pipe_generate_counter += 1
            
            for pipe in self.pipes:
                pipe.update(dt)
                
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)

        self.bird.update(dt)
      
    def drawEverything(self):
        self.win.blit(self.bg_img, (0, -280))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)
        self.win.blit(self.score_text, self.score_text_rect)
        
        if self.is_game_started and not self.is_enter_pressed:
            self.win.blit(self.start_text, self.start_text_rect)
        elif not self.is_game_started:  
            self.win.blit(self.restart_text, self.restart_text_rect)
    
    def restartGame(self):
        self.score = 0 
        self.score_text = self.font.render("Score: 0 ", True, (255, 255, 255))
        self.is_enter_pressed = False 
        self.is_game_started = True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter = 105
        self.bird.is_not_collided = False    
        
    def setupBgAndGround(self):
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor) 
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor) 
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor) 
        
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()
        
        self.ground1_rect.x = 0
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568
        self.ground2_rect.x = self.ground1_rect.rightmage.load("assets/ground.png").convert(), self.scale_factor) 
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor) 
        
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()
        
        self.ground1_rect.x = 0
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568
        self.ground2_rect.x = self.ground1_rect.right