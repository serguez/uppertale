# config.py

WIN_WIDTH = 640
WIN_HEIGHT = 480
FPS = 60
TILESIZE = 32

# Couches (layers)
PLAYER_LAYER = 4
ENTITIES_LAYER = 3
TRANSITION_BLOCK_LAYER = 2
BLOCK_LAYER = 1

PLAYER_SPEED = 6  # équivalent à 3*2

# Couleurs
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# ----------DIALOGUES ET PNJ----------
DIALOGUES = {
    "pnj_1": [
        "Hello World :3",
        "T'es nouveau ?",
        "...",
        "Bon...",
        "Hum... Ton silence est ravissant haha '^^",
        "J'en ai vu plein comme toi, tu sais ?",
        "Je leur répète toujours la même chose:",
        "Tu es un monstre et tu es coincé ici",
        "Tu dois t'échapper grâce à la barrière magique",
        "Tu peux intéragir avec les humains",
        "Eh... Attend ! Tu m'écoute vraiment ?",
        "Tout le monde me prend pour un troll...",
        "C'est gentil de faire semblant, l'ami",
        "Byeeee ^^"
    ],
    "pnj_2": [
        "Bonjo█r",
        "Etrange n'█st-ce pa█ ?",
        "J█ ne sa█s pa███e qui m'arr██e..."
    ],
    "pnj_3":[
        "... ",
        "tu sais euh...",
        "Je ne sais pas ce que tu as fait au petit gus d'avant...",
        "Il n'est pas vraiment méchant... Il veut juste jouer",
        "Fais correctement tes choix la prochaine fois..",
        "Enfin, réfléchis-y..."
    ],
    "pnj_4":[
        "Je peux savoir ce que tu cherches ?",
        "Je te vois là...",
        "Je sais que tu me suis.",
        "Ah... Non ? Bon peut-être alors",
        "C'est vrai que ce village est petit"
        ],
    "pnj_5":[
        "...",
        "Encore ?",
        "Qu'est-ce qui cloche avec toi ?"
        ]
}

PNJ_NAMES = {
    "pnj_1": "Geek Nostalgique :3",
    "pnj_2": "██████",
    "pnj_3": "Hevletica",
    "pnj_4": "Hevletica",
    "pnj_5": "Helvetica"
}

# ----------EXEMPLE DE MOB----------
ENEMY_DATA = {
    1: {
        "name": "Ptit Gus",
        "hp": 25,
        "atq": 3,
        "interaction_options": ["S'informer", "Jouer", "Se moquer"],
        "correct_option_index": 1,
        "description": "C'est juste un enfant...",
        "attacks": {
            "agr": "small",
            "vit": 6,
            "prj": 5,
            "trj": "round6",
            "reb": True,
            "conséquence": "loadmap1_o1"
        }
    },
}

# ----------EXEMPLE DE CARTE----------
# La carte contient des murs "BB", le joueur "XX" et trois PNJ codés "Q1", "Q2" et "Q3".

MAPS_CONFIG = {
    "map1_1": {
        "name": "map1_1",
        "image": "assets/maps/map1_1.png",
        "previous_map": None,            # pas de map précédente pour la première map
        "next_map": ["map1_2"]   # plusieurs chemins possibles
    },
    "map1_2": {
        "name": "map1_2",
        "image": "assets/maps/map1_2.png",
        "previous_map": "map1_1",
        "next_map": ["map1_3", "map1_o1"]  # fin de parcours ou autre suite
    },
    "map1_3": {
        "name": "map1_3",
        "image": "assets/maps/map1_3.png",
        "previous_map": "map1_2",
        "next_map": ["map1_4"]           # par exemple, un unique chemin vers la suite
    },
    "map1_4": {
        "name": "map1_4",
        "image": "assets/maps/map1_4.png",
        "previous_map": "map1_3",
        "next_map": ["map1_5"]
    },
    "map1_5": {
        "name": "map1_5",
        "image": "assets/maps/map1_5.png",
        "previous_map": "map1_4",
        "next_map": ["map1_f"]
    },
    "map1_f": {
        "name": "map1_f",
        "image": "assets/maps/map1_f.png",
        "previous_map": "map1_5",
        "next_map": []
    },
    "map1_o1": {
        "name": "map1_o1",
        "image": "assets/maps/map1_o1.png",
        "previous_map": "map1_2",
        "next_map": ["map1_o2"]
    },
    "map1_o2": {
        "name": "map1_o2",
        "image": "assets/maps/map1_o2.png",
        "previous_map": "map1_o1",
        "next_map": []
    },
}
