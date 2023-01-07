import pygame
from pygame.locals import *
import sys , math ,random,time

tfile = open("media/tilemap.txt","r")
data =  tfile.read()
layers = data.split("\n")
tilemap = []
for layer in layers :
    tilemap.append(list(layer.split(",")))

for layer in tilemap :
    for i in layer :
        if i == ""  :
            layer.remove(i)
tiles = []
y = 0 
for layer in tilemap :
    x = 0 
    for i in layer :
        if i == '1' :
            tiles.append(pygame.Rect(x*16,y*16,16,16))
        x += 1
    y += 1    
def collision_test(tiles,rect):
    collided = []
    for i in tiles :
        if rect.colliderect(i):
            collided.append(i)
    return collided
def move(tiles,ver,hor,rect):
    collision_type = {"top":False,"bottom":False,"right":False,"left":False}
    rect.y += ver
    hit_list = collision_test(tiles,rect)
    for tile in hit_list :
        if ver > 0 :
            rect.bottom = tile.top
            collision_type["bottom"] = True
        if ver< 0 :
            rect.top = tile.bottom
            collision_type["top"] = True
    rect.x += hor
    hit_list = collision_test(tiles,rect)
    for tile in hit_list :
        if hor > 0 :
            rect.right = tile.left
            collision_type["right"] = True
        elif hor < 0 :
            rect.left = tile.right
            collision_type["left"] = True
    
    return collision_type
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
window_width = 500
window_height = 500
survival_button = pygame.image.load("media/survival_button.png")
screen = pygame.display.set_mode((window_width,window_height),0,0)
pygame.display.set_caption("zabba o chta sabba")
start_bn = pygame.image.load("media/start.png")
font = pygame.font.SysFont('Comic Sans MS', 20)
player_img = pygame.image.load("media/player.png")
player_img.set_colorkey((255,255,255))
pd = pygame.image.load("media/down.png")
pd.set_colorkey((255,255,255))
pr= pygame.image.load("media/right.png")
pr.set_colorkey((255,255,255))
pl = pygame.image.load("media/left.png")
pl.set_colorkey((255,255,255))
enemy_img = pygame.image.load("media/enemy.png")
enemy_img.set_colorkey((255,255,255))
wall_img = pygame.image.load("media/wall.png")
bomb_img = pygame.image.load("media/bomb.png")
bomb_img.set_colorkey((255,255,255))
explosion_sound = pygame.mixer.Sound("media/explosion.wav")
damage_sfx = pygame.mixer.Sound("media/death.wav")
#---------------------------------------------------------------------------
empty_tiles = []
y = 0 
for layer in tilemap :
    x = 0 
    for i in layer :
        if i == '0' :
            empty_tiles.append(pygame.Rect(x*16,y*16,16,16))
        x += 1
    y += 1    


# ---- PLAYER CLASS ------------------------------------------------------------
class Player :
    def __init__(self):
        self.moving_foward = False
        self.moving_backward = False
        self.moving_right = False
        self.moving_left = False
        self.verticle_mvmnt = 0
        self.horizantol_mvmnt = 0
        self.health = 3
        self.rect = pygame.Rect(220,200,32,32)
        self.looking_foward = False
        self.looking_backward = False
        self.looking_right = False
        self.looking_left = False
# ------------ VARIABLES  -----------------------------------------------------
player = Player()
nearby = []
for x in empty_tiles :
    if abs(player.rect.x-x.x) < 100 > 50  and abs(player.rect.y-x.y) < 100 > 50 :
        nearby.append(x)
# ------ ENEMY CLASS -----------------------------------------------------------
class Enenmy :
    def __init__(self):
        self.xspeed = 0
        self.yspeed = 0
        self.dx = 0
        self.dy = 0
        self.dist = 0
        self.degree = 0
        self.rect = pygame.Rect(random.choice(nearby).x,random.choice(nearby).y,32,32)
        self.hearts = 3 
        
        
    def angle(self,player_rect):
        
        self.dx, self.dy = player_rect.x - self.rect.x, player_rect.y - self.rect.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.degree = math.atan2(self.dy,self.dx)*(180/math.pi)
        
        
        return [self.dx , self.dy , self.degree,]

class survival_enemy(Enenmy):
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0,500),random.choice((10,470)),32,32)
        self.hearts = 3 

# ------------ GAME CLASS -----------------------------------------------------

lenght = len(empty_tiles)-1
bombs_list = []
for i in range(20):
    bombs_list.append(empty_tiles[random.randint(0,lenght)])

def bombs(player_rect,scroll):
    for x in bombs_list:
        screen.blit(bomb_img,(x.x-scroll[0],x.y-scroll[1]))
        if player_rect.colliderect(x):
            if abs(player_rect.bottom - x.top ) <= 8 :
                game.push_vert = -20
                game.hit = "bottom"
            if abs(player_rect.top - x.bottom ) <= 8 :
                game.push_vert = 20
                game.hit = "top"
            if abs(player_rect.right - x.left) <= 8:
                game.push_hor = -20
                game.hit = "right"
            if abs(player_rect.left - x.right) <= 8 :
                game.push_hor = 20
                game.hit = "left"
            player.health -= 1
            game.hl.remove(game.hl[-1])
            explosion_sound.play()
            bombs_list.remove(x)
class Bullets :
    def __init__(self):
        self.rect = pygame.Rect(player.rect.x+5,player.rect.y+5,10,10)
        self.xmvmnt = 0
        self.ymvmnt = 0
        self.degree = 0
        self.distance = 0
        self.dx = 0
        self.dy = 0  
    def angle(self,mouse_pos):
        self.dx, self.dy = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        self.distance = math.hypot(self.dx, self.dy)
        self.xmvmnt, self.ymvmnt = self.dx / self.distance, self.dy / self.distance
        self.degree = math.atan2(self.dy,self.dx)*(180/math.pi)
    def collided(self):
        for i in game.enemies : 
            if self.rect.colliderect(i.rect) :
                i.hearts -= 1
                game.bullets.remove(self.rect)

heart_img = pygame.image.load("media/heart.png")
heart_img.set_colorkey((255,255,255))
ground = pygame.image.load("media/ground.png")
gun_img = pygame.image.load("media/gun.png")
class Game :
    def __init__ (self):
        self.state = "start"
        self.timer = 200 
        self.enemies = [survival_enemy()]
        self.push_vert = 0
        self.push_hor = 0
        self.score = 0
        self.count = 0
        self.scroll = [0,0]
        self.is_exploded = False
        self.hit = "none"
        self.countdown = 200
        self.hl =[(5,10),(30,10),(55,10)]
        self.last_time = time.time()
        self.dt = 0
        self.last_state = ""
        self.bullets = []

    def start(self):
        screen.blit(start_bn,(141,201.5))
        screen.blit(survival_button,(250-survival_button.get_width(),300))
        if pygame.mouse.get_pos()[0] > 141 and pygame.mouse.get_pos()[0] < 359 :
            if pygame.mouse.get_pos()[1] > 201.5 and pygame.mouse.get_pos()[1] < 298.5 :
                if pygame.mouse.get_pressed()[0]:
                    game.state = "playing"

        if pygame.mouse.get_pos()[0] >142 and pygame.mouse.get_pos()[0] < 250:
            if pygame.mouse.get_pos()[1] > 300 and pygame.mouse.get_pos()[1] < 350 :
                if pygame.mouse.get_pressed()[0]:
                    game.state = "survival_mode"
      
    def playing(self):
        game.scroll[0] += (player.rect.x-game.scroll[0]-242)/20
        game.scroll[1] += (player.rect.y-game.scroll[1]-159)/20
        y = 0 
        for layer in tilemap :
            x = 0 
            for i in layer :
                if i == '0' :
                    screen.blit(ground,(x*16-game.scroll[0],y*16-game.scroll[1]))
                x += 1
            y += 1 
        for i in tiles :
            screen.blit(wall_img,(i.x-game.scroll[0],i.y-game.scroll[1]))
        for enemy in self.enemies :
            if self.countdown <= 0 :
                move(tiles,enemy.angle(player.rect)[1] * 3,enemy.angle(player.rect)[0] * 3,enemy.rect)
            if self.countdown > 0 :
                player.horizantol_mvmnt = 0
                player.verticle_mvmnt = 0
                self.timer = 200
                self.score = 0
                self.countdown -= 1  
            ro_img = pygame.transform.rotate(enemy_img,180-enemy.angle(player.rect)[2])
            ro_img.set_colorkey((255,255,255))
            screen.blit(ro_img,(enemy.rect.x-game.scroll[0],enemy.rect.y-game.scroll[1]))
            enemy.rect.width = (ro_img.get_rect()[2])
            enemy.rect.height = (ro_img.get_rect()[3])
        
            if player.rect.colliderect(enemy.rect):
                if abs(player.rect.bottom - enemy.rect.top ) <= 8 :
                    game.push_vert = -20
                    game.hit = "bottom"
                if abs(player.rect.top - enemy.rect.bottom ) <= 8 :
                    game.push_vert = 20
                    game.hit = "top"
                if abs(player.rect.right - enemy.rect.left) <= 8:
                    game.push_hor = -20
                    game.hit = "right"
                if abs(player.rect.left - enemy.rect.right) <= 8 :
                    game.push_hor = 20
                    game.hit = "left"
                player.health -= 1
                game.hl.remove(game.hl[-1])
                damage_sfx.play()
            if player.health <= 0 :
                self.enemies = []
                self.timer = 200
                enemy.rect.x = 300
                enemy.rect.y = 400
                player.rect.x = 218
                player.rect.y = 218
                self.timer = 0
                game.state = "lose"
                game.last_state = "playing"
                player.health = 3
                game.push_vert = 0
                game.push_hor = 0 
                game.hl = [(5,10),(30,10),(55,10)]
        bombs(player.rect,game.scroll)
        if game.hit != "none":
            player.horizantol_mvmnt = 0
            player.verticle_mvmnt = 0
        if game.hit == "bottom":
            game.push_vert += 0.5
            if game.push_vert == 0 :
                game.hit = "none"
        if game.hit == "top":
            game.push_vert -= 0.5
            if game.push_vert == 0 :
                game.hit = "none"
        if game.hit == "right":
            game.push_vert += 0.5
            if game.push_hor == 0 :
                game.hit = "none"
        if game.hit == "left":
            game.push_vert -= 0.5
            if game.push_hor == 0 :
                game.hit = "none"                          
        if game.push_vert > 0 :
            game.push_vert -= 1
            player.verticle_mvmnt += game.push_vert
        if game.push_vert < 0 :
            game.push_vert += 1
            player.verticle_mvmnt += game.push_vert
        if game.push_hor < 0 :
            game.push_hor += 1
            player.horizantol_mvmnt += game.push_hor
        
        if game.push_hor > 0 :
            game.push_hor -= 1
            player.horizantol_mvmnt += game.push_hor

        self.timer -= 1
        if self.timer <= 0 :   
            self.enemies.append(Enenmy())
            self.timer = 200
        move(tiles,player.verticle_mvmnt,player.horizantol_mvmnt,player.rect)
        player.rect
        player.horizantol_mvmnt = 0
        player.verticle_mvmnt = 0
        game.score += 0.25
        health_text =  font.render(f'{int(game.score)}', False, (0, 0, 50))
        screen.blit(health_text,(5,30))
         
        if player.looking_backward == False and player.looking_foward == False and player.looking_right == False and player.looking_left ==False :
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        
        if player.looking_foward == True and player.moving_left == False and player.moving_right == False:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
        if player.looking_backward == True and player.moving_left == False and player.moving_right == False :
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_left == True and player.moving_backward == False and player.moving_foward == False:
            screen.blit(pl,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_right == True and player.moving_backward == False and player.moving_foward == False :
            screen.blit(pr,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))

        if player.looking_backward == True and player.moving_right == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_backward == True and player.moving_left == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_foward == True and player.moving_left == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
        if player.looking_foward == True and player.moving_right == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
    
        if player.moving_backward == True and player.looking_right == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.moving_backward == True and player.looking_left == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.moving_foward == True and player.looking_left == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
        if player.moving_foward == True and player.looking_right == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1])) 
        for i in game.hl:
            screen.blit(heart_img,(i[0],i[1]))

    def Survival_mode(self) : 
        player.rect.x += player.horizantol_mvmnt
        player.rect.y += player.verticle_mvmnt
        if player.looking_backward == False and player.looking_foward == False and player.looking_right == False and player.looking_left ==False :
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        
        if player.looking_foward == True and player.moving_left == False and player.moving_right == False:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
        if player.looking_backward == True and player.moving_left == False and player.moving_right == False :
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_left == True and player.moving_backward == False and player.moving_foward == False:
            screen.blit(pl,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_right == True and player.moving_backward == False and player.moving_foward == False :
            screen.blit(pr,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))

        if player.looking_backward == True and player.moving_right == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_backward == True and player.moving_left == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.looking_foward == True and player.moving_left == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
        if player.looking_foward == True and player.moving_right == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
    
        if player.moving_backward == True and player.looking_right == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.moving_backward == True and player.looking_left == True:
            screen.blit(pd,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        if player.moving_foward == True and player.looking_left == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))  
        if player.moving_foward == True and player.looking_right == True:
            screen.blit(player_img,(player.rect.x-game.scroll[0],player.rect.y-game.scroll[1]))
        gun_x = pygame.mouse.get_pos()[0] - (player.rect.x+5)-20
        gun_y = pygame.mouse.get_pos()[1] - (player.rect.y+5)-2.5
        degree = math.atan2(gun_y,gun_x)*(180/math.pi)
        rotated_gun_img = pygame.transform.rotate(gun_img,180-degree)
        screen.blit(rotated_gun_img,(player.rect.x+5,player.rect.y+5))
        
        for i in self.bullets : 
            pygame.draw.rect(screen,(255,255,255),i.rect)
            i.rect.x += i.xmvmnt*5
            i.rect.y += i.ymvmnt*5
            i.collided()
        for enemy in self.enemies :
            enemy_i = pygame.transform.rotate(enemy_img,180-enemy.angle(player.rect)[2])
            enemy_i.set_colorkey((255,255,255))
            screen.blit(enemy_i,enemy.rect)
            enemy.rect.x +=  enemy.angle(player.rect)[0] * 2
            enemy.rect.y += enemy.angle(player.rect)[1] * 2
            if enemy.hearts <= 0 :
                game.enemies.remove(enemy)
            if enemy.rect.colliderect(player.rect) :
                player.health -= 0.2
            if player.health <= 0 :
                player.health = 3 
                self.enemies = [survival_enemy()]
                game.last_state = "survival_mode"
                game.state = "lose"
        self.timer -= 1 
        if self.timer <= 0 :
            self.enemies.append(survival_enemy())
            self.timer= 50

    def restat(self):
        score_text =  font.render(f'Your scoore : {int(game.score)}', False, (0, 0, 0))
        screen.blit(score_text,(180,250))
        restart_text =  font.render('Click To Restart', False, (0, 0, 0))
        screen.blit(restart_text,(180,200))
        if pygame.mouse.get_pressed()[0]:
            game.score = 0
            self.countdown = 200
            game.hit = "none"
            game.state = game.last_state

game = Game()
while True :
    screen.fill((45, 45, 46))
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit(0)
        if event.type == KEYDOWN :
            if event.key == K_w :
                player.moving_foward = True
                player.looking_foward = True
                player.looking_backward = False
                player.looking_right = False
                player.looking_left = False
            if event.key == K_s :
                player.moving_backward = True
                player.looking_foward = False
                player.looking_backward = True
                player.looking_right = False
                player.looking_left = False
            if event.key == K_d :
                player.moving_right = True
                player.looking_foward = False
                player.looking_backward = False
                player.looking_right = True
                player.looking_left = False
            if event.key == K_a :
                player.moving_left = True
                player.looking_foward = False
                player.looking_backward = False
                player.looking_right = False
                player.looking_left = True
 
        if event.type == KEYUP :
            if event.key == K_w :
                player.moving_foward = False
                player.verticle_mvmnt = 0
            if event.key == K_s :
                player.moving_backward = False
                player.verticle_mvmnt = 0
            if event.key == K_d :
                player.moving_right = False
                player.horizantol_mvmnt = 0
            if event.key == K_a :
                player.moving_left = False
                player.horizantol_mvmnt = 0
        if event.type == MOUSEBUTTONUP : 
            if game.state == "survival_mode" :
                b = Bullets()
                b.angle(pygame.mouse.get_pos())
                game.bullets.append(b)
    
    if player.moving_foward == True :
        player.verticle_mvmnt = -4
    if player.moving_backward == True :
        player.verticle_mvmnt = 4
    if player.moving_right == True :
        player.horizantol_mvmnt = 4
    if player.moving_left == True :
        player.horizantol_mvmnt = -4
    if game.state == "start":
        game.start()
    if game.state == "playing":
        game.playing()
    if game.state == "lose":
        game.restat()
    if game.state == "survival_mode":
        game.Survival_mode()
    

    clock.tick(60)
    pygame.display.update()