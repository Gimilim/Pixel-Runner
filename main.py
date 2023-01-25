from random import choice, randint
from sys import exit

import pygame

# Settings.
WIDTH = 800
HEIGHT = 400
WINDOW_SIZE = (WIDTH, HEIGHT)
GAME_ACTIVE = False
PLAY_DEATH = False
GROUND_LEVEL = 300
ENEMIES_SPEED = 5
PLAYER_POSITION = (50, GROUND_LEVEL)  # Bottomleft (x, y)
FLY_BOTTOM = 210
SNAIL_BOTTOM = GROUND_LEVEL
OBSTACLE_SPAWN_RANGE = [900, 1100]
DEATH_JUMP_FORCE = 5
PLAYER_JUMP_FORCE = 20

# Images.
PLAYER_WALK_1 = 'graphics/Player/Player_walk_1.png'
PLAYER_WALK_2 = 'graphics/Player/Player_walk_2.png'
PLAYER_JUMP = 'graphics/Player/Player_jump.png'
PLAYER_STAND = 'graphics/Player/Player_stand.png'

FLY_1 = 'graphics/Fly/Fly_1.png'
FLY_2 = 'graphics/Fly/Fly_2.png'

SNAIL_1 = 'graphics/Snail/Snail_1.png'
SNAIL_2 = 'graphics/Snail/Snail_2.png'

SKY = 'graphics/Sky.png'
GROUND = 'graphics/Ground.png'


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

        self.death_jump = DEATH_JUMP_FORCE

    def animation_state(self):
        if self.rect.bottom < GROUND_LEVEL:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_LEVEL:
            self.gravity = -PLAYER_JUMP_FORCE

    def aply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

    def play_death(self):
        self.rect.y -= self.death_jump
        self.death_jump -= 0.1
        if self.rect.top >= HEIGHT:
            return False
        return True

    def update(self):
        if PLAY_DEATH:
            return self.play_death()
        else:
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


class Background(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type
        if self.type == 'ground':
            ground_state_1 = (0, GROUND_LEVEL)
            ground_state_2 = (-8, GROUND_LEVEL)
            self.ground_states = [ground_state_1, ground_state_2]
            self.ground_index = 0

            self.image = pygame.image.load(GROUND).convert()
            self.rect = self.image.get_rect(
                topleft=self.ground_states[self.ground_index]
            )
        else:
            self.image = pygame.image.load(SKY).convert()
            self.rect = self.image.get_rect(topleft=(0, 0))

    def animation_state(self):
        if self.type == 'ground':
            self.ground_index += 0.1
            if self.ground_index >= len(self.ground_states):
                self.ground_index = 0
            self.rect = self.ground_states[int(self.ground_index)]

        return None

    def update(self):
        self.animation_state()

        return None


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(
        f'Score: {current_time}', False, (64, 64, 64)
    )
    score_rect = score_surf.get_rect(center=(400, 50))

    screen.blit(score_surf, score_rect)

    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player_group.sprite, obstacle_group, False):
        return False
    else:
        return True


pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption('~:*_Pixel Runner_*:~')

clock = pygame.time.Clock()

score = 0

# Menu.
player_stand_surf = pygame.image.load(PLAYER_STAND).convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(400, 210))

# Groups.
background_group = pygame.sprite.Group()
background_group.add(Background('ground'), Background('sky'))

player_group = pygame.sprite.GroupSingle()
player_sprite = Player()
player_group.add(player_sprite)

obstacle_group = pygame.sprite.Group()

# Font.
game_font = pygame.font.Font('Font/Pixeltype.ttf', 50)

# Timer.
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)

# Main Game Loop.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

        if GAME_ACTIVE:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_ACTIVE = True

    if GAME_ACTIVE:
        # Update and Draw.
        background_group.update()
        background_group.draw(screen)

        player_group.update()
        player_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        score = display_score()

        GAME_ACTIVE = collision_sprite()
        PLAY_DEATH = not GAME_ACTIVE
    else:
        # Death animation.
        if PLAY_DEATH:
            player_group.update()
            PLAY_DEATH = player_sprite.update()

            background_group.draw(screen)
            obstacle_group.draw(screen)
            player_group.draw(screen)

            score_surf = game_font.render(
                f'Score: {score}', False, (64, 64, 64)
            )
            score_rect = score_surf.get_rect(center=(400, 50))
            screen.blit(score_surf, score_rect)
        else:
            player_sprite.death_jump = DEATH_JUMP_FORCE
            obstacle_group.empty()

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
                game_name_surf = game_font.render(
                    'Pixel Runner', False, 'Gold'
                )
                game_name_surf = pygame.transform.rotozoom(
                    game_name_surf, 0, 1.5
                )
                game_name_rect = game_name_surf.get_rect(center=(400, 70))

                screen.blit(game_name_surf, game_name_rect)

            hint_surf = game_font.render(
                'Press SPACE to start.', False, 'Gold'
            )
            hint_rect = hint_surf.get_rect(center=(400, 350))

            screen.blit(hint_surf, hint_rect)

        start_time = int(pygame.time.get_ticks() / 1000)

    pygame.display.update()
    clock.tick(60)


# Add pause option
# Increase difficult with increasing time
# Add main class
# Add settings file
