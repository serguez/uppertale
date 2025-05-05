# sprites.py

import pygame
from config import *
from event_manager import Event

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.mouvement()
        self.collide_exit_block()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def mouvement(self):
        # On désactive les mouvements pendant un dialogue
        if self.game.dialogue_manager.dialogue_open:
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = "down"

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_exit_block(self):
        hits_exit = pygame.sprite.spritecollide(self, self.game.exit_blocks, False)
        for block in hits_exit:
            # Si c'est une Door verrouillée, on ignore
            if hasattr(block, "locked") and block.locked:
                continue
            self.game.load_new_map(block.target_map)
            break   

class Pnj(pygame.sprite.Sprite):
    def __init__(self, game, x, y, pnj_id):
        self.game = game
        self._layer = ENTITIES_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.pnj_id = pnj_id
        self.type = "pnj"

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Ennemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, ennemy_id=0):
        self.game = game
        self._layer = ENTITIES_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.ennemy_id = ennemy_id
        self.type = "ennemy"

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Transition_Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target_map):
        self.game = game
        self._layer = TRANSITION_BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.exit_blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.target_map = target_map

class Trigger(pygame.sprite.Sprite):
    """Zone invisible ou levier ; déclenche un event quand le joueur appuie sur E dessus."""
    def __init__(self, game, x, y, kind, event_id):
        super().__init__(game.all_sprites)
        self.game, self.kind, self.event_id = game, kind, event_id
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(topleft=(x*TILESIZE, y*TILESIZE))

    def activate(self):
        self.game.event_mgr.post(Event(self.kind, {"id": self.event_id}))

class Lever(Trigger):
    def __init__(self, game, x, y, lever_id):
        super().__init__(game, x, y, "LEVER_PULLED", lever_id)
        self.on_img  = pygame.Surface((TILESIZE, TILESIZE)); self.on_img.fill((180,90,0))
        self.off_img = pygame.Surface((TILESIZE, TILESIZE)); self.off_img.fill((100,50,0))
        self.image   = self.off_img
        self.pulled  = False

    def activate(self):
        if not self.pulled:
            self.pulled = True
            self.image  = self.on_img
            self.game.lever_states[self.event_id] = True
            super().activate()

class Door(Transition_Block):
    def __init__(self, game, x, y, target_map, unlock_id):
        super().__init__(game, x, y, target_map)
        self.locked = True
        self.image.fill((150,150,150))           # gris = fermé
        game.event_mgr.subscribe("LEVER_PULLED", self.on_event)
        self.unlock_id = unlock_id
        if game.lever_states.get(self.unlock_id, False):
            self.locked = False
            self.image.fill(GREEN)

    def on_event(self, event):
        if event.payload["id"] == self.unlock_id:
            self.locked = False
            self.image.fill(GREEN)               # vert = ouvert

    # on override la collision pour ignorer si verrouillée
    def collide_player(self, player_rect):
        return (not self.locked) and self.rect.colliderect(player_rect)

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("assets/fonts/shadow.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
        return False
