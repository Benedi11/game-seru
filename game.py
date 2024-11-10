from pygame import *
from random import randint

mixer.init()
mixer.music.load(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\space.ogg")
mixer.music.play()
fire_sound = mixer.Sound(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\fire.ogg")

#untuk pembuatatan font
font.init()
font1 = font.Font(None, 80)
win = font1.render("YOU WIN", True, (255,255,255))
lost = font1.render("YOU LOST", True, (180,0,0))
font2 = font.Font(None, 36)

#buat background music
img_back = r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\back.jpg"
img_hero = r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\rocket.png"
img_enemy = r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\ufo.png"
img_tembak = r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\bullet.png"
score =0
lost = 0
max_lost = 5
goal = 15

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#kelas penerus untuk sprite pemain (dikontrol oleh panah)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < min_width - 80:
            self.rect.x += self.speed
    def fire(self):
        pass

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > min_height:
            self.rect.x = randint(80, min_width -80)
            self.rect.y = 0
            lost = lost+1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()


min_width = 700
min_height = 500
window = display.set_mode((min_width, min_height))
display.set_caption("Shooter")
background = transform.scale(image.load(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\back.jpg"), (min_width, min_height))

#karakter game akan ditampilkan
pesawat = Player(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\rocket.png", 5, min_height-100, 100,100,10)
aliens = sprite.Group()
for i in range(1,6):
    alien = Enemy(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\ufo.png", randint(80, min_width-80), -40, 80,50, randint(1,5))
    aliens = alien()

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if not finish:
        #perbaharui background dan pemain
        window.blit(background, (0,0))
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        pesawat.update()
        aliens.update()

        pesawat.reset()
        aliens.draw(window)
        
        collides = sprite.groupcollide(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\ufo.png", r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\bullet.png", True, True)
        for c in collides:
            # this loop will be repeated as many times as monsters are killed
            score = score + 1
            monster = Enemy(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\ufo.png", randint(80, min_width - 80), -40, 80, 50, randint(1, 5))
            img_enemy.add(monster)

        # possible loss: missed too many or the character collided with the enemy
        if sprite.spritecollide(r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\rocket.png", r"C:\Users\userpc\Downloads\shooter game (1)\shooter game\ufo.png", False) or lost >= max_lost:
            finish = True # lost, set the background and no more sprite control.
            window.blit(lost, (200, 200))

        # win check: how many points did you score?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    # the loop runs every 0.05 seconds
    time.delay(50)
