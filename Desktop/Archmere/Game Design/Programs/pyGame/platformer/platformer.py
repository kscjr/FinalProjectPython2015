# side scrolling platformer

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    level = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()

    def update(self):
        self.calc_grav()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0
        

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0



class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class platform2(Platform):

    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None
    level = None

    def update(self):
        self.rect.x += self.change_x

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right
        self.rect.y += self.change_y

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y< 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.rect.top = self.rect.bottom

        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
                self.change_y *= -1
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
                self.change_x *=-1 
        
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

class Level():
    level = "0"
    platform_list = None
    enemy_list = None

    world_shift = 0

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        

        background_image = pygame.image.load("marioBackground.jpg")
        background_fit = pygame.transform.scale(background_image, (800, 600))       

        screen.blit(background_fit, [0, 0])
    
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.level_limit = -1000

        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 [120, 500, 1700, 200]]

        enemylist = [[105, 35, 100, 100],
                     [105, 35, 200, 200]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        block = platform2(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        for enemy in enemylist:
            block = Enemy(enemy[0], enemy[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.enemy_list.add(block)

class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.level_limit = -1000

        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 [120, 500, 1700, 200]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        block = platform2(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

class Level_03(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.level_limit = -1000

        level = [[210, 10, 475, 470],
                 [210, 10, 800, 320],
                 [210, 10, 900, 420],
                 [210, 10, 1020, 180],
                 [120, 500, 1700, 200]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        block = platform2(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_04(Level):
    def __init__(self, player):

        
        
        Level.__init__(self, player)

        self.level_limit = -1000




def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    level_list.append(Level_04(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done == True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.go_left()
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.go_right()
                if event.key == pygame.K_UP or event.key == ord('w'):
                    player.jump()

            if event.type == pygame.KEYUP:
                if player.change_x != 0:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.stop()
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.stop()

        active_sprite_list.update()

        current_level.update()



        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
        
