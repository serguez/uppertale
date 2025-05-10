# dialogue.py
import pygame
from config import WIN_WIDTH, WIN_HEIGHT, WHITE

class DialogueManager:
    def __init__(self, game, dialogues, names, dialogue_font, pnj_name_font):
        """
        Initialise le gestionnaire de dialogues.
        :param game: Référence vers l'objet principal du jeu.
        :param dialogues: Dictionnaire des dialogues, indexé par pnj_id.
        :param names: Dictionnaire des noms des PNJ, indexé par pnj_id.
        :param dialogue_font: Police pour le texte des dialogues.
        :param pnj_name_font: Police pour afficher le nom du PNJ.
        """
        self.game = game
        self.dialogues = dialogues
        self.names = names
        self.dialogue_font = dialogue_font
        self.pnj_name_font = pnj_name_font

        self.dialogue_open = False
        self.current_dialogue_lines = []
        self.current_line_index = 0
        self.current_pnj_id = None

    def start_dialogue(self, pnj_id):
        """
        Démarre le dialogue pour le PNJ identifié par pnj_id.
        """
        if pnj_id in self.dialogues:
            self.current_dialogue_lines = self.dialogues[pnj_id]
            self.current_line_index = 0
            self.dialogue_open = True
            self.current_pnj_id = pnj_id

    def advance_dialogue(self):
        """
        Passe à la ligne suivante du dialogue et ferme le dialogue si terminé.
        """
        if not self.dialogue_open:
            return

        self.current_line_index += 1
        if self.current_line_index >= len(self.current_dialogue_lines):
            self.dialogue_open = False
            self.current_dialogue_lines = []
            self.current_line_index = 0
            self.current_pnj_id = None

    def draw(self, screen):
        """
        Affiche la boîte de dialogue et le texte courant sur l'écran.
        """
        if not self.dialogue_open:
            return

        dialogue_box = pygame.Rect(50, WIN_HEIGHT - 150, WIN_WIDTH - 100, 100)
        pygame.draw.rect(screen, (50, 50, 50), dialogue_box)

        # nouveau comportement : n’affiche le nom que si c’est un vrai PNJ
        if self.current_pnj_id in self.names:
            npc_name   = self.names[self.current_pnj_id]
            name_surf  = self.pnj_name_font.render(npc_name, True, WHITE)
            screen.blit(name_surf, (dialogue_box.x + 10, dialogue_box.y + 10))
            y_offset = dialogue_box.y + 10 + name_surf.get_height() + 5
        else:
            # pas de nom à afficher
            y_offset = dialogue_box.y + 10

        # on affiche ensuite le texte, aligné selon s’il y a un nom ou non
        current_line  = self.current_dialogue_lines[self.current_line_index]
        wrapped_lines = self.wrap_text(current_line, self.dialogue_font, dialogue_box.width - 20)
        line_height   = self.dialogue_font.get_linesize()
        for line in wrapped_lines:
            text_surface = self.dialogue_font.render(line, True, WHITE)
            screen.blit(text_surface, (dialogue_box.x + 10, y_offset))
            y_offset += line_height

    def wrap_text(self, text, font, max_width):
        """
        Découpe le texte pour qu'il ne dépasse pas la largeur max.
        :param text: Texte à découper.
        :param font: Police utilisée pour mesurer le texte.
        :param max_width: Largeur maximale autorisée.
        :return: Liste de lignes découpées.
        """
        words = text.split()
        wrapped_lines = []
        current_line = ""
        for word in words:
            test_line = word if current_line == "" else current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)
        return wrapped_lines

if __name__ == "__main__":
    # Test indépendant du DialogueManager
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    dialogue_font = pygame.font.SysFont("Arial", 16)
    pnj_name_font = pygame.font.SysFont("Arial", 24)

    dialogues = {
        "pnj_1": [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        ],
        "pnj_2": [
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
            "Ex ea commodo consequat."
        ]
    }
    names = {
        "pnj_1": "NPC Un",
        "pnj_2": "NPC Deux"
    }

    dm = DialogueManager(None, dialogues, names, dialogue_font, pnj_name_font)
    dm.start_dialogue("pnj_1")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dm.advance_dialogue()

        screen.fill((30, 30, 30))
        dm.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
