import pygame
import sys
import os
import math
import sys
from sprites import *
from config import *
from dialogue import DialogueManager
from combat import CombatManager
from event_manager import EventManager
from map_converter import convert_map_image
import time
from pygame.math import Vector2

def wrap_text(text, font, max_width):
    words = text.split()
    wrapped_lines = []
    current_line = ""
    for word in words:
        test_line = word if not current_line else current_line + " " + word
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    return wrapped_lines

class Game:
    def __init__(self):
        pygame.init()
        self.event_mgr = EventManager() 
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
#                                               flags=pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.font = pygame.font.Font("assets/fonts/shadow.ttf", 32)
        self.dialogue_font = pygame.font.Font("assets/fonts/HomeVideo-BLG6G.ttf", 16)
        self.pnj_name_font = pygame.font.Font("assets/fonts/HomeVideo-BLG6G.ttf", 24)
        
        self.intro_background = pygame.image.load("assets/sprites/introbackground.png")
        self.tutoriel_background = pygame.image.load("assets/sprites/tutoriel.png") 
        self.cinematic_act2 = pygame.image.load("assets/sprites/cinematic_act2.png")
        self.cinematic_outro = pygame.image.load("assets/sprites/outro.png")
        self.cinematic_gameover = pygame.image.load("assets/sprites/gameoverscreen.png")
        self.cinematic_act1 = pygame.image.load("assets/sprites/cinematic_act1.png")

        levier1 = pygame.image.load("assets/sprites/levier1.png").convert_alpha()
        levier2 = pygame.image.load("assets/sprites/levier2.png").convert_alpha()
        self.levier1 = pygame.transform.scale(levier1, (TILESIZE, TILESIZE))
        self.levier2 = pygame.transform.scale(levier2, (TILESIZE, TILESIZE))

        door = pygame.image.load("assets/sprites/lock.png").convert_alpha()
        self.door = pygame.transform.scale(door, (TILESIZE, TILESIZE))

        entity = pygame.image.load("assets/sprites/entity.png").convert_alpha()
        self.entity = pygame.transform.scale(entity, (TILESIZE, TILESIZE))

        player = pygame.image.load("assets/sprites/player.png").convert_alpha()
        player_act3 = pygame.image.load("assets/sprites/player_act3.png").convert_alpha()
        self.player = pygame.transform.scale(player, (TILESIZE, TILESIZE))
        self.player_act3 = pygame.transform.scale(player_act3, (TILESIZE, TILESIZE))

        wall_act1 = pygame.image.load("assets/sprites/bush.png").convert_alpha()
        wall_act2 = pygame.image.load("assets/sprites/wall.png").convert_alpha()
        wall_act3 = pygame.image.load("assets/sprites/wallact3.png").convert_alpha()
        self.wall_texture_act1 = pygame.transform.scale(wall_act1, (TILESIZE, TILESIZE))
        self.wall_texture_act2 = pygame.transform.scale(wall_act2, (TILESIZE, TILESIZE))
        self.wall_texture_act3 = pygame.transform.scale(wall_act3, (TILESIZE, TILESIZE))

        exit = pygame.image.load("assets/sprites/exit.png").convert_alpha()
        self.exit = pygame.transform.scale(exit, (TILESIZE, TILESIZE))

        # Création du gestionnaire de dialogue avec les données de config
        from config import DIALOGUES, PNJ_NAMES
        self.dialogue_manager = DialogueManager(self, DIALOGUES, PNJ_NAMES, self.dialogue_font, self.pnj_name_font)

        self.maps_config = MAPS_CONFIG

        self.lever_states = {}
        self.levers = pygame.sprite.Group()
        self.door_states = {}

        self.background = None

        self.current_act = "act1"
        
    def createTileMap(self, map_data):
        player_coordonne = [0, 0]
        offset = [10, 7.5]

        for y, ligne in enumerate(map_data):
            for x, code in enumerate(ligne):
                if code == "XX":
                    player_coordonne = [x, y]
        # Calcul de l'offset pour recentrer la carte
        x_diff = player_coordonne[0] - offset[0]
        y_diff = player_coordonne[1] - offset[1]

        for i, row in enumerate(map_data):
            for j, code in enumerate(row):
                x = j - x_diff
                y = i - y_diff
                if code == "BB":
                    Block(self, x, y)
                elif code == "XX":
                    Player(self, x, y)
                elif code == "BACK":
                    # Création d'une porte de retour si elle est définie dans la config
                    if self.current_map_config["previous_map"]:
                        Transition_Block(self, x, y, target_map=self.current_map_config["previous_map"])
                elif code.startswith("NEXT_"):
                    # Extraction de l'index dans la liste des maps suivantes
                    index = int(code.split("_")[1])
                    if index < len(self.current_map_config["next_map"]):
                        target = self.current_map_config["next_map"][index]
                        Transition_Block(self, x, y, target_map=target)
                elif code.startswith("Q"):
                    pnj_number = code[1:]
                    pnj_id = "pnj_" + pnj_number
                    Pnj(self, x, y, pnj_id=pnj_id)
                    
                elif code.startswith("EN"):
                    ennemy_id = code[2:]
                    Ennemy(self, x, y, ennemy_id=ennemy_id)
                    
                elif code.startswith("LEVER_"):
                    lever_id = int(code.split("_")[1])
                    Lever(self, x, y, lever_id)
                elif code.startswith("DOOR_"):
                    door_id = int(code.split("_")[1])
                    Door(self, x, y, door_id)

    def load_new_map(self, map_key):
        self.all_sprites.empty()
        self.blocks.empty()
        self.exit_blocks.empty()

        self.current_map_config = self.maps_config.get(map_key)
        if not self.current_map_config:
            print("Map inconnue:", map_key)
            return
        print("[DEBUG] Map", map_key)

        bg_path = self.current_map_config.get("background")
        if bg_path:
            bg = pygame.image.load(bg_path).convert()
            # 1) on récupère l'ancienne taille
            w, h = bg.get_size()
            # 2) on scale ×4
            bg = pygame.transform.scale(bg, (w * 5 ,h * 5)) 
            # on stocke et on positionne le Rect à (-1000, -1000)
            self.background = bg
            self.bg_rect = bg.get_rect(topleft=(-1000, -1000))
        else:
            # si pas de background défini, on remplit en noir
            self.background = None
            self.bg_rect = pygame.Rect(0,0,0,0)
        
        bg_sprite = pygame.sprite.Sprite()
        bg_sprite._layer  = 0                        # couche la plus basse
        bg_sprite.groups  = self.all_sprites         # l’ajoute à all_sprites
        pygame.sprite.Sprite.__init__(bg_sprite, self.all_sprites)
        bg_sprite.image = bg                          # surface du fond
        bg_sprite.rect  = bg.get_rect(topleft=(-1000,-1000))

        self.current_map = convert_map_image(self.current_map_config["image"])
        self.createTileMap(self.current_map)

    def new(self):
        # Démarrage d'une nouvelle partie
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.exit_blocks = pygame.sprite.LayeredUpdates()
        self.levers = pygame.sprite.Group()

        self.load_new_map("map1_1")
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Touche d'interaction pour lancer le dialogue
                if event.key == pygame.K_e:
                    self.try_interact()
                # Avancer le dialogue avec SPACE s'il est ouvert
                if event.key == pygame.K_SPACE and self.dialogue_manager.dialogue_open:
                    self.dialogue_manager.advance_dialogue()

    def try_interact(self):
        player = next((s for s in self.all_sprites if isinstance(s, Player)), None)
        if not player:
            return

        INTER_RANGE = 50
        for lever in self.levers:
            # transforme les tuples en vecteurs
            player_pos = Vector2(player.rect.center)
            lever_pos  = Vector2(lever.rect.center)
            if player_pos.distance_to(lever_pos) < INTER_RANGE:
                lever.pull()
                return

        player_sprite = None
        for spr in self.all_sprites:
            if isinstance(spr, Player):
                player_sprite = spr
                break
        if not player_sprite:
            return
        
        nearest_entity = None
        min_dist = float('inf')
        INTERACTION_RANGE = 50
        # Parcourt toutes les entités pouvant interagir (PNJ et Ennemis)
        for spr in self.all_sprites:
            if isinstance(spr, Pnj) or isinstance(spr, Ennemy):
                dist = math.hypot(spr.rect.centerx - player_sprite.rect.centerx,
                                  spr.rect.centery - player_sprite.rect.centery)
                if dist < INTERACTION_RANGE and dist < min_dist:
                    min_dist = dist
                    nearest_entity = spr
        if nearest_entity:
            if isinstance(nearest_entity, Pnj):
                # Lance le dialogue si c'est un PNJ
                self.dialogue_manager.start_dialogue(nearest_entity.pnj_id)
                print("PNJ")
            elif isinstance(nearest_entity, Ennemy):
                # si pas encore tué, on lance le combat
                if not ENEMY_DATA[int(nearest_entity.ennemy_id)]["has_been_killed"]:
                    from combat import start_combat
                    outcome = start_combat(nearest_entity, self)
                else:
                    # sinon, on affiche un petit dialogue “vide”
                    self.dialogue_manager.current_dialogue_lines = ["… mais personne n'est venu."]
                    self.dialogue_manager.current_line_index = 0
                    self.dialogue_manager.dialogue_open = True
                    self.dialogue_manager.current_pnj_id = None

    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        self.screen.blit(self.background, self.bg_rect)

        self.all_sprites.draw(self.screen)
        self.dialogue_manager.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    
    def intro_screen(self):
        intro = True
        title = self.font.render("DEAD OUTSIDE THEORY", True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 70, 140, 50, WHITE, BLACK, "JOUER", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
        
    def tutoriel(self):
        tuto = True
        
        while tuto:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tuto = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tuto = False
            self.screen.blit(self.tutoriel_background, (0, 0))
            self.clock.tick(FPS)
            pygame.display.update()
    
    def cinematic(self, id):
        cinem = True
        
        while cinem:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cinem = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if id ==2:
                            pygame.quit()
                            sys.exit()
                        if id==3:
                            pygame.quit()
                            sys.exit()
                        else:
                            cinem = False  
            if id == 1:
                self.screen.blit(self.cinematic_act2, (0, 0))
                self.current_act = "act3"
                print("[DEBUG] Passage à l'acte 3")
                self.load_new_map("map1_18")
            if id == 2:
                self.screen.blit(self.cinematic_outro, (0, 0))
            elif id == 3:
                self.screen.blit(self.cinematic_gameover, (0, 0))
            elif id ==4:
                self.screen.blit(self.cinematic_act1, (0, 0))
            else:
                print("[DEBUG] Id de cinématic reçu inconnu : ", id)

            self.clock.tick(FPS)
            pygame.display.update()

    

g = Game()
g.intro_screen()
g.tutoriel()
g.cinematic(4)
g.new()
while g.running:
    g.main()

pygame.quit()
sys.exit()
