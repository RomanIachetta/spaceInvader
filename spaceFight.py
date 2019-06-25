import pygame
import time
import random
import sys

global score
score = 0
global done
done = False
class Shot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image = pygame.transform.rotate(self.image, -90)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.y -= 3

        def enemy(self):
            self.rect.y += 6

class EnemyShot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image = pygame.transform.rotate(self.image, -90)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.y += 3

        def enemy(self):
            self.rect.y += 6
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 700
    def update(self):
        if pygame.key.get_pressed()[pygame.K_a]and self.rect.x > 0:
            self.rect.x -= 5
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.x < 770:
            self.rect.x += 5



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 60


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 550

height = 800
width = 800
clock = pygame.time.Clock()
pygame.init()
font = pygame.font.SysFont("comicsansms", 30)
screen = pygame.display.set_mode([width, height])
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
backg = pygame.transform.scale(pygame.image.load('backg.jpg').convert(), (width, height))
def main():

    global done

    pygame.display.set_caption("Space Fight")



    player = Player()
    enemy = Enemy()

    player_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()

    for i in range(60):
        wall = Wall()
        wall.rect.x = wall.rect.x + i * 25
        if i % 6 == 0:
            wall.rect.x += 100
        if i >=30:
            wall.rect.y = wall.rect.y + 29
            wall.rect.x = wall.rect.x - 750

        all_sprites_list.add(wall)
        wall_list.add(wall)
    for i in range(30):
        enemy1 = Enemy()
        enemy1.rect.x = enemy1.rect.x + i * 50
        if i > 9 and i < 20:
            enemy1.rect.y = enemy1.rect.y + 40
            enemy1.rect.x = enemy1.rect.x - 500
        if i > 19:
            enemy1.rect.y = enemy1.rect.y + 80
            enemy1.rect.x = enemy1.rect.x - 1000

        all_sprites_list.add(enemy1)
        enemy_list.add(enemy1)

    player_list.add(player)
    enemy_list.add(enemy)
    all_sprites_list.add(player)
    all_sprites_list.add(enemy)

    global score
    while not done:
        screen.fill(WHITE)
        screen.blit(backg, (0, 0))
        text = font.render("Score " + str(score), True, (WHITE))

        screen.blit(text, (720 - text.get_width() // 2, 40 - text.get_height() // 2))

        for enemy in enemy_list:
            if enemy.rect.y != 800:
                enemy.rect.x += 2
                if enemy.rect.x == 700:
                    enemy.rect.x = 10
                    enemy.rect.y += 40
                if enemy.rect.x % random.randint(50,700) ==0:
                    shot1 = EnemyShot()
                    # Set the bullet so it is where the player is
                    shot1.rect.x = enemy.rect.x + 11
                    shot1.rect.y = enemy.rect.y
                    # Add the bullet to the lists
                    all_sprites_list.add(shot1)
                    enemy_bullet_list.add(shot1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                # Fire a bullet if the user clicks the mouse button
                shot = Shot()
                # Set the bullet so it is where the player is
                shot.rect.x = player.rect.x + 11
                shot.rect.y = player.rect.y
                # Add the bullet to the lists
                all_sprites_list.add(shot)
                bullet_list.add(shot)



        for bullet in bullet_list:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
            wall_hit_list = pygame.sprite.spritecollide(bullet, wall_list, True)
            if wall_hit_list:
                bullet.kill()
            if enemy_hit_list:
                bullet.kill()
                score+=1

        for bullet in enemy_bullet_list:
            wall_hit_list = pygame.sprite.spritecollide(bullet, wall_list, True)
            player_hit = pygame.sprite.spritecollide(bullet, player_list, True)
            if wall_hit_list:
                bullet.kill()
            if player_hit:
                done = True
        for enemy in enemy_list:
            player_hit =  pygame.sprite.spritecollide(enemy, player_list, True)
            if player_hit:
                done = True
        if len(enemy_list) == 0:
            done = True

        player.update()
        all_sprites_list.update()
        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def endScreen():
    global done
    while True:
        screen.fill(WHITE)
        screen.blit(backg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                done = False



        text = font.render("Score " + str(score), True, (WHITE))
        screen.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    if pygame.key.get_pressed()[pygame.K_l]:
        done = False
    main()
    endScreen()



