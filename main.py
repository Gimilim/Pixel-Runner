from random import choice, randint
from sys import exit

import pygame

WINDOW_SIZE = (800, 400)
GAME_ACTIVE = False
ENEMIES_SPEED = 5
PLAYER_POSITION = (50, 300)  # Bottomleft
FLY_BOTTOM = 210
SNAIL_BOTTOM = 300
OBSTACLE_SPAWN_RANGE = [900, 1100]

# Images
PLAYER_WALK_1 = 'graphics/Player/Player_walk_1.png'
PLAYER_WALK_2 = 'graphics/Player/Player_walk_2.png'
PLAYER_JUMP = 'graphics/Player/Player_jump.png'

FLY_1 = 'graphics/Fly/Fly_1.png'
FLY_2 = 'graphics/Fly/Fly_2.png'

SNAIL_1 = 'graphics/Snail/Snail_1.png'
SNAIL_2 = 'graphics/Snail/Snail_2.png'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(PLAYER_WALK_1).convert_alpha()
        player_walk_2 = pygame.image.load(PLAYER_WALK_2).convert_alpha()
        self.player_jump = pygame.image.load(PLAYER_JUMP).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(bottomleft=(PLAYER_POSITION))
        self.gravity = 0

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def aply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.aply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load(FLY_1).convert_alpha()
            fly_2 = pygame.image.load(FLY_2).convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = FLY_BOTTOM
        else:
            snail_1 = pygame.image.load(SNAIL_1).convert_alpha()
            snail_2 = pygame.image.load(SNAIL_2).convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = SNAIL_BOTTOM

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(*OBSTACLE_SPAWN_RANGE), y_pos)
        )

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= ENEMIES_SPEED
        self.destroy()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(
        f'Score: {current_time}', False, (64, 64, 64)
    )
    score_rect = score_surf.get_rect(center=(400, 50))

    screen.blit(score_surf, score_rect)

    return current_time


def enemies_movement(enemies_rect_list):
    if enemies_rect_list:
        for enemies_rect in enemies_rect_list:
            enemies_rect.x -= ENEMIES_SPEED

            if enemies_rect.bottom == 300:
                screen.blit(snail_surf, enemies_rect)
            else:
                screen.blit(fly_surf, enemies_rect)

        enemies_rect_list = [
            enemie for enemie in enemies_rect_list if enemie.x > -100
        ]

        return enemies_rect_list
    else:
        return []


def collisions(player, enemies_rect_list):
    if enemies_rect_list:
        for enemie_rect in enemies_rect_list:
            if player.colliderect(enemie_rect):
                return False
    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

    return None


pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('~:*_Pixel Runner_*:~')

clock = pygame.time.Clock()

score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Font
game_font = pygame.font.Font('Font/Pixeltype.ttf', 50)

# BackGround
sky_surf = pygame.image.load('graphics/Sky.png').convert()
sky_rect = sky_surf.get_rect(topleft=(0, 0))

ground_surf = pygame.image.load('graphics/Ground.png').convert()

# ground_rect = ground_surf.get_rect(topleft=(0, 300))
ground_rect_1 = ground_surf.get_rect(topleft=(0, 300))
ground_rect_2 = ground_surf.get_rect(topleft=(-8, 300))
ground_rects = [ground_rect_1, ground_rect_2]
ground_index = 0
ground_rect = ground_rects[ground_index]

# Player
player_walk_1 = pygame.image.load(
    'graphics/Player/Player_walk_1.png'
).convert_alpha()
player_walk_2 = pygame.image.load(
    'graphics/Player/Player_walk_2.png'
).convert_alpha()

player_walk = [player_walk_1, player_walk_2]

player_jump = pygame.image.load(
    'graphics/Player/Player_jump.png'
).convert_alpha()

player_index = 0

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(10, 300))

player_stand_surf = pygame.image.load(
    'graphics/Player/Player_stand.png'
).convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)

player_stand_rect = player_stand_surf.get_rect(center=(400, 210))
player_gravity = 0

# Enemies

# Snail
snail_frame_1 = pygame.image.load('graphics/Snail/Snail_1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/Snail/Snail_2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly_1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly_2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

enemies_rect_list = []

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

ground_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(ground_animation_timer, 200)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

        if GAME_ACTIVE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
                if randint(0, 2):
                    enemies_rect_list.append(
                        snail_surf.get_rect(
                            bottomright=(randint(900, 1100), 300)
                        )
                    )

                else:
                    enemies_rect_list.append(
                        fly_surf.get_rect(
                            bottomright=(randint(900, 1100), 210)
                        )
                    )

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0

                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0

                fly_surf = fly_frames[fly_frame_index]

            if event.type == ground_animation_timer:
                if ground_index == 0:
                    ground_index = 1
                else:
                    ground_index = 0

                ground_rect = ground_rects[ground_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_ACTIVE = True

    if GAME_ACTIVE:
        # BackGround
        screen.blit(sky_surf, sky_rect)
        screen.blit(ground_surf, ground_rect)

        # Score
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()
        screen.blit(player_surf, player_rect)

        # test
        player.update()
        player.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)
        # test

        # Enemies Movement
        enemies_rect_list = enemies_movement(enemies_rect_list)

        GAME_ACTIVE = collisions(player_rect, enemies_rect_list)

    else:
        enemies_rect_list = []
        player_rect = player_surf.get_rect(bottomleft=(10, 300))
        player_gravity = 0

        screen.fill((94, 129, 162))
        screen.blit(player_stand_surf, player_stand_rect)

        game_over_surf = game_font.render('Game Over', False, 'Gold')
        game_over_surf = pygame.transform.rotozoom(game_over_surf, 0, 2)
        game_over_rect = game_over_surf.get_rect(center=(400, 50))

        if score > 0:
            score_surf = game_font.render(f'Score: {score}', False, 'Gold')
            score_surf = pygame.transform.rotozoom(score_surf, 0, 1)
            score_rect = score_surf.get_rect(center=(400, 95))

            screen.blit(game_over_surf, game_over_rect)
            screen.blit(score_surf, score_rect)
        else:
            game_name_surf = game_font.render('Pixel Runner', False, 'Gold')
            game_name_surf = pygame.transform.rotozoom(game_name_surf, 0, 1.5)
            game_name_rect = game_name_surf.get_rect(center=(400, 70))

            screen.blit(game_name_surf, game_name_rect)

        hint_surf = game_font.render('Press SPACE to start', False, 'Gold')
        hint_rect = hint_surf.get_rect(center=(400, 350))

        screen.blit(hint_surf, hint_rect)

        start_time = int(pygame.time.get_ticks() / 1000)

    pygame.display.update()
    clock.tick(60)


# Добавить паузу
# Добавить анимацию "смерти" (персонаж подпрыгивает и падает под землю)
# Добавить ускорение противников со временем
