import pygame, sys, random, math
from config import *
from event_manager import Event

pygame.font.init()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

# --- Fonction utilitaire pour dessiner un dégradé ---
def draw_gradient_rect(surface, rect):
    x, y, w, h = rect
    mid = w // 2
    for i in range(w):
        if i < mid:
            t = i / mid
            r = int(t * 255)
            g = int((1 - t) * 255)
        else:
            t = (i - mid) / mid
            r = int((1 - t) * 255)
            g = int(t * 255)
        color = (r, g, 0)
        pygame.draw.line(surface, color, (x + i, y), (x + i, y + h))

# --- Classe Button ---
class Button:
    def __init__(self, rect, text, color=GRAY, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.rendered = font.render(text, True, text_color)
        self.rendered_rect = self.rendered.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered, self.rendered_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- Classe Monster ---
class Monster:
    def __init__(self, data):
        self.name = data.get("name", "Inconnu")
        self.max_hp = data.get("hp", 50)
        self.hp = self.max_hp
        self.atq = data.get("atq", 5)
        self.interaction_options = data.get("interaction_options", [])
        self.correct_option_index = data.get("correct_option_index", 0)
        self.correct_option_text = data.get("correct_option_text")
        self.incorrect_option_text = data.get("incorrect_option_text")
        self.correct_interaction_done = False
        self.description = data.get("description", "Inconnu")
        self.attacks = data.get("attacks", {})
        self.consequence = self.attacks.get("conséquence")
        print(f"[DEBUG] Monster.consequence = {self.consequence}")

# --- Classe Projectile ---
class Projectile:
    def __init__(self, x, y, size, speed, angle, trajectory, rebounds):
        self.size = size
        self.speed = speed
        self.trajectory = trajectory
        self.rebounds = rebounds
        self.age = 0
        
        if self.trajectory.startswith("round"):
            if len(self.trajectory) > 5:
                try:
                    circle_value = int(self.trajectory[5:])
                except ValueError:
                    circle_value = 5
            else:
                circle_value = 5
            self.circle_radius = circle_value * 10
            self.center_x = x
            self.center_y = y
            self.angle = random.uniform(0, 2 * math.pi)
            self.pos_x = self.center_x + self.circle_radius * math.cos(self.angle)
            self.pos_y = self.center_y + self.circle_radius * math.sin(self.angle)
            self.angular_velocity = self.speed / self.circle_radius if self.circle_radius != 0 else 0
        elif self.trajectory == "sinus":
            self.pos_x = x
            self.pos_y = y
            self.base_x = x
            self.base_y = y
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)
            self.phase = 0
            self.amplitude = 20
            norm = math.sqrt(self.vx**2 + self.vy**2)
            self.perp_vx = -self.vy / norm if norm != 0 else 0
            self.perp_vy = self.vx / norm if norm != 0 else 0
        elif self.trajectory == "zigzag":
            self.pos_x = x
            self.pos_y = y
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)
            self.zigzag_timer = 0
            self.zigzag_interval = 30
        else:  # "linear" et autres
            self.pos_x = x
            self.pos_y = y
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)
            self.angle = angle
        
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size, self.size)
    
    def update(self, arena_rect):
        self.age += 1
        if self.trajectory.startswith("round"):
            self.angle += self.angular_velocity
            self.pos_x = self.center_x + self.circle_radius * math.cos(self.angle)
            self.pos_y = self.center_y + self.circle_radius * math.sin(self.angle)
        elif self.trajectory == "sinus":
            self.base_x += self.vx
            self.base_y += self.vy
            self.phase += 0.1
            offset = self.amplitude * math.sin(self.phase)
            self.pos_x = self.base_x + self.perp_vx * offset
            self.pos_y = self.base_y + self.perp_vy * offset
        elif self.trajectory == "zigzag":
            self.pos_x += self.vx
            self.pos_y += self.vy
            self.zigzag_timer += 1
            if self.zigzag_timer >= self.zigzag_interval:
                self.vy = -self.vy
                self.zigzag_timer = 0
        else:
            self.pos_x += self.vx
            self.pos_y += self.vy
        
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size, self.size)
        
        active = True
        if not self.trajectory.startswith("round"):
            if self.rect.left < arena_rect.left or self.rect.right > arena_rect.right:
                if self.rebounds:
                    self.vx = -self.vx
                else:
                    active = False
            if self.rect.top < arena_rect.top or self.rect.bottom > arena_rect.bottom:
                if self.rebounds:
                    self.vy = -self.vy
                else:
                    active = False
        return active
    
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# --- Classe CombatManager ---
class CombatManager:
    def __init__(self, game, screen, monster):
        self.game = game
        self.screen = screen
        self.monster = monster
        self.player_hp = 20
        self.state = "menu"   # États : "menu", "combat", "interaction", "pity", "wait", "enemy_turn", "end"
        self.outcome = None   # "victoire", "défaite", "fuite", "épargné"
        self.message = ""
        self.combat_finished = False
        self.wait_start_time = None  # Pour le délai en état "wait"
        self.init_menu()
        self.skip_victory_screen = False
    
    # Pour définir un message et passer en état "wait"
    def set_message_and_wait(self, message):
        self.message = message
        self.wait_start_time = pygame.time.get_ticks()
        self.state = "wait"
    
    # Initialisation du menu principal
    def init_menu(self):
        self.menu_buttons = []
        btn_width = 150
        btn_height = 50
        spacing = 20
        total_width = 3 * btn_width + 2 * spacing
        start_x = (WIN_WIDTH - total_width) // 2
        y = WIN_HEIGHT - btn_height - 20
        self.menu_buttons.append(Button((start_x, y, btn_width, btn_height), "Combat"))
        self.menu_buttons.append(Button((start_x + btn_width + spacing, y, btn_width, btn_height), "Interagir"))
        self.menu_buttons.append(Button((start_x + 2*(btn_width + spacing), y, btn_width, btn_height), "Pitié"))
        self.message = ""
    
    def init_interaction_menu(self):
        self.interaction_buttons = []
        base_btn_width = 250
        base_btn_height = 50
        base_spacing = 20
        n = len(self.monster.interaction_options)
        total_width = n * base_btn_width + (n - 1) * base_spacing
        if total_width > WIN_WIDTH:
            scale_factor = WIN_WIDTH / total_width
            btn_width = int(base_btn_width * scale_factor)
            btn_height = int(base_btn_height * scale_factor)
            spacing = int(base_spacing * scale_factor)
        else:
            btn_width = base_btn_width
            btn_height = base_btn_height
            spacing = base_spacing
        total_width = n * btn_width + (n - 1) * spacing
        start_x = (WIN_WIDTH - total_width) // 2
        y = WIN_HEIGHT - btn_height - 20
        for opt in self.monster.interaction_options:
            self.interaction_buttons.append(Button((start_x, y, btn_width, btn_height), opt))
            start_x += btn_width + spacing
        self.message = ""
    
    def init_pity_menu(self):
        self.pity_buttons = []
        btn_width = 150
        btn_height = 50
        spacing = 20
        total_width = 2 * btn_width + spacing
        start_x = (WIN_WIDTH - total_width) // 2
        y = WIN_HEIGHT - btn_height - 20
        self.pity_buttons.append(Button((start_x, y, btn_width, btn_height), "Fuir"))
        self.pity_buttons.append(Button((start_x + btn_width + spacing, y, btn_width, btn_height), "Épargner"))
        self.message = ""
    
    def draw_player_hp_bar(self):
        if self.skip_victory_screen:
            pass
        else:
            bar_width = 300
            bar_height = 20
            x = WIN_WIDTH // 2 - bar_width // 2
            y = WIN_HEIGHT - 95
            pygame.draw.rect(self.screen, RED, (x, y, bar_width, bar_height))
            life_fraction = self.player_hp / 20
            remaining_width = int(bar_width * life_fraction)
            pygame.draw.rect(self.screen, YELLOW, (x, y, remaining_width, bar_height))
            pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 2)

    def draw_monster_hp_bar(self):
        if self.skip_victory_screen:
            pass
        else:
            bar_width = 300
            bar_height = 20
            x = 20
            y = 50
            pygame.draw.rect(self.screen, DARK_GRAY, (x, y, bar_width, bar_height))
            life_fraction = self.monster.hp / self.monster.max_hp
            remaining_width = int(bar_width * life_fraction)
            pygame.draw.rect(self.screen, RED, (x, y, remaining_width, bar_height))
            pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 2)
    
    def update(self, events):
        if self.state == "menu":
            self.update_menu(events)
        elif self.state == "combat":
            self.update_combat(events)
        elif self.state == "interaction":
            self.update_interaction(events)
        elif self.state == "pity":
            self.update_pity(events)
        elif self.state == "wait":
            # En état "wait", on attend 2 secondes
            if pygame.time.get_ticks() - self.wait_start_time >= 2000:
                if self.outcome is None:
                    self.start_enemy_turn()
                    self.state = "enemy_turn"
                else:
                    self.state = "end"
        elif self.state == "enemy_turn":
            self.update_enemy_turn(events)
        elif self.state == "end":
            self.update_end(events)
        
        if self.message:
            msg_surface = small_font.render(self.message, True, YELLOW)
            self.screen.blit(msg_surface, (WIN_WIDTH // 2 - msg_surface.get_width() // 2, WIN_HEIGHT - 40))
    
        if self.monster.hp <= 0 and self.state != "end":
            self.outcome = "victoire"
            self.state = "end"
            if self.monster.consequence:
                self._process_consequence(self.monster.consequence)
        if self.player_hp <= 0 and self.state != "end":
            self.skip_victory_screen = True
            self.game.cinematic(3)
            pygame.quit()
            sys.exit()
    
    def draw(self):
        if self.skip_victory_screen:
            pass
        else:
            self.screen.fill(BLACK)
            monster_text = font.render(self.monster.name, True, WHITE)
            self.screen.blit(monster_text, (20, 20))
            self.draw_monster_hp_bar()
            self.draw_player_hp_bar()

            if self.state == "menu":
                for btn in self.menu_buttons:
                    btn.draw(self.screen)
            elif self.state == "combat":
                self.draw_combat()
            elif self.state == "interaction":
                for btn in self.interaction_buttons:
                    btn.draw(self.screen)
            elif self.state == "pity":
                for btn in self.pity_buttons:
                    btn.draw(self.screen)
            elif self.state == "enemy_turn":
                self.draw_enemy_turn()
            elif self.state == "end":
                self.draw_end()

            if self.message:
                msg_surface = small_font.render(self.message, True, YELLOW)
                self.screen.blit(msg_surface, (WIN_WIDTH // 2 - msg_surface.get_width() // 2, WIN_HEIGHT - 40))
    
    def update_menu(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.menu_buttons:
                    if btn.is_clicked(pos):
                        if btn.text == "Combat":
                            self.start_bagarre()
                        elif btn.text == "Interagir":
                            self.start_interaction()
                        elif btn.text == "Pitié":
                            self.start_pity()
    
    def start_bagarre(self):
        self.state = "combat"
        self.combat_start_time = pygame.time.get_ticks()
        self.combat_duration = 2000
        self.combat_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 - 25, 300, 50)
        self.combat_line_x = self.combat_rect.left
        self.combat_finished = False
        self.combat_damage = 0
    
    def update_combat(self, events):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.combat_start_time
        progress = min(elapsed / self.combat_duration, 1)
        self.combat_line_x = self.combat_rect.left + int(progress * self.combat_rect.width)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.combat_finished:
                    center_x = self.combat_rect.centerx
                    error = abs(self.combat_line_x - center_x)
                    max_damage = 15
                    damage = max(0, int(max_damage * (1 - error / (self.combat_rect.width / 2))))
                    self.combat_damage = damage
                    self.monster.hp = max(self.monster.hp - damage, 0)
                    self.message = f"Vous infligez {damage} dégâts !"
                    self.combat_finished = True
                    self.wait_start_time = pygame.time.get_ticks()
                    self.state = "wait"
        if elapsed >= self.combat_duration and not self.combat_finished:
            self.message = "Vous avez raté l'attaque !"
            self.combat_finished = True
            self.wait_start_time = pygame.time.get_ticks()
            self.state = "wait"
    
    def draw_combat(self):
        draw_gradient_rect(self.screen, self.combat_rect)
        pygame.draw.rect(self.screen, WHITE, self.combat_rect, 2)
        pygame.draw.line(self.screen, RED, (self.combat_line_x, self.combat_rect.top),
                         (self.combat_line_x, self.combat_rect.bottom), 3)
        instr = small_font.render("Appuyez sur SPACE au bon moment !", True, WHITE)
        self.screen.blit(instr, (WIN_WIDTH // 2 - instr.get_width() // 2, self.combat_rect.bottom + 10))
    
    def start_interaction(self):
        self.state = "interaction"
        self.init_interaction_menu()
    
    def update_interaction(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(self.interaction_buttons):
                    if btn.is_clicked(pos):
                        if btn.text == self.monster.interaction_options[0]:
                            self.message = f"{self.monster.name} : {self.monster.hp}PV & {self.monster.atq}ATQ. {self.monster.description}"
                        else:
                            if i == self.monster.correct_option_index:
                                self.message = self.monster.correct_option_text
                                self.monster.correct_interaction_done = True
                            else:
                                self.message = self.monster.incorrect_option_text
                        self.wait_start_time = pygame.time.get_ticks()
                        self.state = "wait"
    
    def start_pity(self):
        self.state = "pity"
        self.init_pity_menu()
    
    def update_pity(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.pity_buttons:
                    if btn.is_clicked(pos):
                        if btn.text == "Fuir":
                            flee_factor = random.random()
                            if flee_factor < 0.5:
                                self.message = "Vous avez réussi à fuir !"
                                self.wait_start_time = pygame.time.get_ticks()
                                self.outcome = "fuite"
                                self.state = "wait"
                            else:
                                self.message = "Fuite ratée."
                                self.wait_start_time = pygame.time.get_ticks()
                                self.state = "wait"
                        elif btn.text == "Épargner":
                            if self.monster.correct_interaction_done:
                                self.message = "Vous l'avez épargné."
                                self.wait_start_time = pygame.time.get_ticks()
                                self.outcome = "épargné"
                                self.state = "wait"
                                if self.monster.consequence:
                                    self._process_consequence(self.monster.consequence)
                            else:
                                self.message = "Vous ne pouvez pas l'épargner !"
                                self.wait_start_time = pygame.time.get_ticks()
                                self.state = "wait"
    
    def start_enemy_turn(self):
        self.enemy_turn_start = pygame.time.get_ticks()
        self.enemy_turn_duration = 3000
        self.arena_rect = pygame.Rect(50, 100, WIN_WIDTH - 100, WIN_HEIGHT - 200)
        self.player_rect = pygame.Rect(self.arena_rect.centerx - 15, self.arena_rect.centery - 15, 30, 30)
        self.projectiles = self.generate_projectiles()
    
    def generate_projectiles(self):
        proj_list = []
        att = self.monster.attacks
        size_map = {"small": 20, "mid": 35, "high": 50}
        proj_size = size_map.get(att.get("agr", "mid"), 35)
        speed = att.get("vit", 5)
        n_proj = att.get("prj", 1)
        traj = att.get("trj", "linear")
        rebounds = att.get("reb", True)
        for i in range(n_proj):
            if traj.startswith("round"):
                x = random.randint(self.arena_rect.left + proj_size, self.arena_rect.right - proj_size)
                y = random.randint(self.arena_rect.top + proj_size, self.arena_rect.bottom - proj_size)
                angle = 0
            else:
                edge = random.choice([0, 1, 2, 3])
                if edge == 0:
                    x = random.randint(self.arena_rect.left, self.arena_rect.right - proj_size)
                    y = self.arena_rect.top
                    angle = random.uniform(math.radians(45), math.radians(135))
                elif edge == 1:
                    x = random.randint(self.arena_rect.left, self.arena_rect.right - proj_size)
                    y = self.arena_rect.bottom - proj_size
                    angle = random.uniform(math.radians(225), math.radians(315))
                elif edge == 2:
                    x = self.arena_rect.left
                    y = random.randint(self.arena_rect.top, self.arena_rect.bottom - proj_size)
                    angle = random.uniform(math.radians(-45), math.radians(45))
                else:
                    x = self.arena_rect.right - proj_size
                    y = random.randint(self.arena_rect.top, self.arena_rect.bottom - proj_size)
                    angle = random.uniform(math.radians(135), math.radians(225))
            proj = Projectile(x, y, proj_size, speed, angle, traj, rebounds)
            proj_list.append(proj)
        return proj_list
    
    def update_enemy_turn(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += 5
        if keys[pygame.K_UP]:
            self.player_rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.player_rect.y += 5
        if self.player_rect.left < self.arena_rect.left:
            self.player_rect.left = self.arena_rect.left
        if self.player_rect.right > self.arena_rect.right:
            self.player_rect.right = self.arena_rect.right
        if self.player_rect.top < self.arena_rect.top:
            self.player_rect.top = self.arena_rect.top
        if self.player_rect.bottom > self.arena_rect.bottom:
            self.player_rect.bottom = self.arena_rect.bottom

        active_projectiles = []
        for proj in self.projectiles:
            active = proj.update(self.arena_rect)
            if self.player_rect.colliderect(proj.rect):
                self.player_hp = max(self.player_hp - self.monster.atq, 0)
                self.message = f"Vous subissez {self.monster.atq} dégâts !"
                pygame.display.flip()
                active = False
            if active:
                active_projectiles.append(proj)
        self.projectiles = active_projectiles

        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_turn_start >= self.enemy_turn_duration:
            self.state = "menu"
            self.init_menu()
    
    def draw_enemy_turn(self):
        pygame.draw.rect(self.screen, WHITE, self.arena_rect, 2)
        pygame.draw.rect(self.screen, GREEN, self.player_rect)
        for proj in self.projectiles:
            proj.draw(self.screen)
    
    def update_end(self, events):
        for event in events:
            if event.type == pygame.KEYUP:
                self.state = "exit"
                break
    
    def draw_end(self):
        if self.skip_victory_screen:
            pass
        else:
            if self.outcome == "victoire":
                end_text = font.render("Victoire !", True, WHITE)
            elif self.outcome == "défaite":
                end_text = font.render("Défaite...", True, WHITE)
            elif self.outcome == "fuite":
                end_text = font.render("Vous avez fui !", True, WHITE)
            elif self.outcome == "épargné":
                end_text = font.render("Epargné !", True, WHITE)
            else:
                end_text = font.render("Fin du combat", True, WHITE)
            self.screen.blit(end_text, (WIN_WIDTH // 2 - end_text.get_width() // 2, WIN_HEIGHT // 2 - end_text.get_height() // 2))
            instr = small_font.render("Appuyez sur une touche pour quitter", True, WHITE)
            self.screen.blit(instr, (WIN_WIDTH // 2 - instr.get_width() // 2, WIN_HEIGHT // 2 + end_text.get_height()))
    
    def run(self):
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.state == "end":
                self.draw()
                pygame.display.flip()
                waiting = True
                while waiting:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
                        self.state = "exit"
                break
            else:
                self.update(events)
                self.draw()
                pygame.display.flip()
                clock.tick(FPS)
        return self.outcome
    
    def _process_consequence(self, consequence_str: str):
        if consequence_str.startswith("load"):
            # tout ce qu'il y a après "load"
            map_key = consequence_str[len("load"):]
            if map_key == "map1_12":
                self.game.current_act = "act2"
                print("[DEBUG] Passage à l'acte 2")
            self.game.load_new_map(map_key)
            
        
        elif consequence_str.startswith("opendoor_"):
            # décode l'id après "opendoor_"
            door_id_str = consequence_str.split("_", 1)[1]
            try:
                door_id = int(door_id_str)
                # poste un événement global
                # 1) Persister l’ouverture pour les futures salles
                self.game.door_states[door_id] = True
                # 2) Poster l’événement pour la porte actuelle (si elle existe)
                print(f"[DEBUG] Marking door {door_id} open persistently and posting event")
                from event_manager import Event
                self.game.event_mgr.post(Event("OPEN_DOOR", {"door_id": door_id}))
            except ValueError:
                print(f"[Consequence] id de porte invalide : {door_id_str!r}")

        elif consequence_str.startswith("cinematic_"):
            self.skip_victory_screen = True
            cinematic_id = consequence_str.split("_", 1)[1]
            self.game.cinematic(int(cinematic_id))
        else:
            # debug, cas non prévu
            print(f"[Consequence] action inconnue: {consequence_str!r}")


def start_combat(ennemy, game):
    overlay = pygame.Surface(game.screen.get_size())
    game.screen.blit(overlay, (0,0))
    pygame.display.flip()

    from config import ENEMY_DATA
    enemy_data = ENEMY_DATA.get(int(ennemy.ennemy_id))
    monster = Monster(enemy_data)
    combat_manager = CombatManager(game, game.screen, monster)
    outcome = combat_manager.run()

    if outcome == "victoire":
        ENEMY_DATA[int(ennemy.ennemy_id)]["has_been_killed"] = True
        ennemy.killed = True
        ennemy.kill()
    elif outcome == "défaite":
        print("PERDU")
        pygame.quit()
        sys.exit()

    return outcome
