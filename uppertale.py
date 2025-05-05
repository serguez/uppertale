# uppertale.py

import pygame
import math
import sys
from sprites import *
from config import *
from dialogue import DialogueManager
from combat import CombatManager
from event_manager import EventManager
from map_converter import convert_map_image
import time
import sprites


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

        # Création du gestionnaire de dialogue avec les données de config
        from config import DIALOGUES, PNJ_NAMES
        self.dialogue_manager = DialogueManager(self, DIALOGUES, PNJ_NAMES, self.dialogue_font, self.pnj_name_font)

        self.maps_config = MAPS_CONFIG

        self.event_mgr = EventManager()
        self.lever_states = {}
        
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

                prefix = code[:2]

                if prefix in TRIGGERS:
                    cfg = TRIGGERS[prefix]
                    cls = getattr(sprites, cfg["class_name"])
                    # construis les kwargs à partir de cfg["args"] et de code
                    kwargs = { cfg["args"][0]: code }
                    cls(self, x, y, **kwargs)

                elif prefix in REACTIONS:
                    cfg = REACTIONS[prefix]
                    cls = getattr(sprites, cfg["class_name"])
                    # par exemple :
                    kwargs = {
                        cfg["args"][0]: self.current_map_config["next_map"][0],
                        cfg["args"][1]: code.replace("DR", "LV")
                    }
                    cls(self, x, y, **kwargs)
        
    def load_new_map(self, map_key):
        print(f"[DEBUG] current_map_config for {map_name} → {self.current_map_config!r}")
        self.all_sprites.empty()
        self.blocks.empty()
        self.exit_blocks.empty()

        self.current_map_config = self.maps_config.get(map_key)
        if not self.current_map_config:
            print("Map inconnue:", map_key)
            return
        self.current_map = convert_map_image(self.current_map_config["image"])
        self.createTileMap(self.current_map)

    def new(self):
        # Démarrage d'une nouvelle partie
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.exit_blocks = pygame.sprite.LayeredUpdates()

        self.current_map_config = self.maps_config["map1_1"]
        self.current_map = convert_map_image(self.current_map_config["image"])
        self.createTileMap(self.current_map)

        self.lever_states.clear()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Touche d'interaction pour lancer le dialogue
                if event.key == pygame.K_e:
                    self.try_talk_to_entities()
                # Avancer le dialogue avec SPACE s'il est ouvert
                if event.key == pygame.K_SPACE and self.dialogue_manager.dialogue_open:
                    self.dialogue_manager.advance_dialogue()

    def try_talk_to_entities(self):
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
                # Récupère l'id de l'ennemi
                enemy_id = int(nearest_entity.ennemy_id)
                print(enemy_id)
                # Récupère les données de l'ennemi depuis config.py
                from combat import start_combat
                outcome = start_combat(nearest_entity, self)
        if nearest_entity is None:
            for spr in self.all_sprites:
                if isinstance(spr, Trigger):
                    dist = math.hypot(spr.rect.centerx - player_sprite.rect.centerx,
                                      spr.rect.centery - player_sprite.rect.centery)
                    if dist < INTERACTION_RANGE:
                        spr.activate()
                        return

    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # Affiche la boîte de dialogue si elle est ouverte
        self.dialogue_manager.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    
    def game_over(self):
        pass
    
    def intro_screen(self):
        intro = True
        title = self.font.render("UPPERTALE", True, BLACK)
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
            
        

g = Game()
g.intro_screen()
g.tutoriel()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
