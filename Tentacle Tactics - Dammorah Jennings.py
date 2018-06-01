# Imports
import pygame
import random
import os

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Tentical Tactics"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LAVENDER = (195, 141, 239)
PINK = (255, 186, 233)
PURPLE = (99, 45, 226)

# Fonts
FONT_SM = pygame.font.Font('images/Athena of the Ocean.ttf', 24)
FONT_MD = pygame.font.Font('images/Athena of the Ocean.ttf', 32)
FONT_LG = pygame.font.Font('images/Athena of the Ocean.ttf', 180)
# Images

ship_img = pygame.image.load('images/TT-p-ship-1.png')
laser_img = pygame.image.load('images/bullet-1.png')
mob_img = pygame.image.load('images/TT-M1-1.png')
bomb_img = pygame.image.load('images/TT-M-bullets-1.png')
mob2_img = pygame.image.load('images/TT-M2-1.png')
bg_image = pygame.image.load('images/bg-1.png')
start_img = pygame.image.load('images/start_bg.png')
end_img = pygame.image.load('images/end-bg.png')


healthbar5 = pygame.image.load('images/healthbar-1.png')
healthbar4 = pygame.image.load('images/healthbar4-1.png')
healthbar3 = pygame.image.load('images/healthbar3-1.png')
healthbar2 = pygame.image.load('images/healthbar2-1.png')
healthbar1 = pygame.image.load('images/healthbar1-1.png')







# Sounds
EXPLOSION = pygame.mixer.Sound('images/explosion.ogg')
ZAP = pygame.mixer.Sound('images/player-zap.ogg')
EW = pygame.mixer.Sound('images/squish.ogg')
SPLAT = pygame.mixer.Sound('images/splat.ogg')


L1_MUSIC = pygame.mixer.Sound('images/Fox-wedding.ogg')
START_MUSIC = pygame.mixer.Sound('images/Psycho-Pass.ogg')
END_MUSIC = pygame.mixer.Sound('images/Departures-Blessing.ogg')

L1_MUSIC.play(-1)
# Stages
START = 0
PLAYING = 1
END = 2
PAUSE = 3


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()


        b_loc = (0, 715)
        b_loc2 = (50, 715)
        b_loc3 = (100, 715)
        b_loc4 = (150, 715)
        b_loc5 = (200, 715)



        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 6
        self.shield = 5

    
    def move_left(self):
        self.rect.x -= self.speed

        
    def move_right(self):
        self.rect.x += self.speed


    def shoot(self):


        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        ZAP.play()

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            SPLAT.play()
            self.shield -= 1


        if self.shield == 5:
            screen.blit(healthbar5,(0, 730))

        if self.shield == 4:
            screen.blit(healthbar4,(0, 730))

        if self.shield == 3:
            screen.blit(healthbar3,(0, 730))

        if self.shield == 2:
            screen.blit(healthbar2,(0, 730))

        if self.shield == 1:
            screen.blit(healthbar1,(0, 730))

        if self.shield == 0:
            stage == END

            


        hit_list = pygame.sprite.spritecollide(self, mobs, False)

        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()
            stage == END

        if self.rect.x < -10:
            self.rect.x = -10
        elif self.rect.x > 830:
            self.rect.x = 830




class Laser(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5      

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
            stage == END







 #mob 1   
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        EW.play()

        

    def update(self, laser, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += 150
            self.kill()
            






#mob2
class Mob2(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.shield = 3

   
    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        EW.play()

        

    def update(self, laser, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)


        for hit in hit_list:
            self.shield -= 1

        if len(hit_list) > 0:
            self.shield = 0
    
        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += 150
            
        if self.shield == 0:
            self.kill()
            player.score += 150



            

#bomb1
class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 6

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()





#fleet 1        
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32


        if mobs == 0:
            stage == END

            
    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()





            


# Make game objects
def setup():
    screen.blit(bg_image,(0, 0))

    ticks = 0

    
    global player, mobs, bombs, fleet, ship, lasers, stage

    ship = Ship(384, 536, ship_img)

    mob1 = Mob(128, 64, mob_img)
    mob2 = Mob(228, 64, mob_img)
    mob3 = Mob(328, 64, mob_img)
    mob4 = Mob(428, 64, mob_img)
    mob5 = Mob(528, 64, mob_img)
    mob6 = Mob(128, -64, mob_img)
    mob7 = Mob(228, -64, mob_img)
    mob8 = Mob(328, -64, mob_img)
    mob9 = Mob(428, -64, mob_img)
    mob10 = Mob(528, -64, mob_img)
    mob11 = Mob2(128, -184, mob2_img)
    mob12 = Mob2(228, -184, mob2_img)
    mob13 = Mob2(328, -184, mob2_img)
    mob14 = Mob2(428, -184, mob2_img)
    mob15 = Mob2(528, -184, mob2_img)
    mob16 = Mob2(128, -184, mob2_img)
    mob17 = Mob2(228, -184, mob2_img)
    mob18 = Mob2(328, -184, mob2_img)
    mob19 = Mob2(428, -184, mob2_img)
    mob20 = Mob2(528, -184, mob2_img)




    


    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11, mob12, mob13, mob14, mob15, mob16, mob17, mob18, mob19, mob20)

    bombs = pygame.sprite.Group()



    fleet = Fleet(mobs)


# set stage
stage = START


    
#Game Helper functions
def show_title_screen():
    screen.blit(start_img,(0, 0))
    title_text = FONT_LG.render("Tentical Tactics!!!", 1, WHITE)
    screen.blit(title_text, [228, 204])
    

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])


def show_end():
    screen.blit(end_img, (0, 0))
    
    title_text = FONT_LG.render("press 'r' to restart", 1, WHITE)
    screen.blit(title_text, [228, 204])

    title_text = FONT_LG.render("press 'x' to exit", 1, WHITE)
    screen.blit(title_text, [228, 284])


    title_text = FONT_LG.render("press 's' for score", 1, WHITE)
    screen.blit(title_text, [228, 344])

def display_stats():
    title_text = FONT_LG.render(str(player.score), 1, WHITE)
    screen.blit(title_text, [228, 204])


    
# Game loop


tick = 0
frame = 0
setup()

done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

    if stage == PLAYING:
        screen.blit(bg_image,(0, 0))
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        if mobs == 0:
            stage = END

            
    if stage == END:
        show_end() 
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_r]:
            stage = START
            
        if pressed[pygame.K_s]:
            display_stats()

        if pressed[pygame.K_x]:
            exit()



        


    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()


    if stage == PLAYING:    
        if len(player) == 0:
            stage = END
        if len(mobs) == 0:
            stage = END        

    tick += 1
    if tick%10 == 0:
        frame += 1
        if frame > 8:
            frame = 0
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)
    



    

    if stage == START:
        show_title_screen()
        
    if mobs == 0:
        stage = END

        
    # Update screen (Actually draw the picture in the window.)

    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
