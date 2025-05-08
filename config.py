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

PLAYER_SPEED = 6

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
        "Bonjour petit robot",
        "Tu cherches à passer ?",
        "...",
        "Bon...",
        "Hum... Ton silence est ravissant haha '^^",
        "Il y a un bouton je crois en haut à gauche du parc, il ouvre le portail pour aller dans l'école. ",
        "Byeeee ^^"
    ],
    "pnj_2": [
        "Euh...",
        "Salut ?"
    ],
    "pnj_3":[
        "Quel drôle de création..."
    ],
    "pnj_4":[
        "Bas les pattes !",
        ],
    "pnj_5":[
        "Oh un robot...",
        ],
    "pnj_6":[
        "...",
        "[REMOVED BY THE SYSTEM]... C'est toi ?",
        "Tu es obligé de te cacher avec un robot... ?",
        "Meme si je viens devant chez toi ?",
        "Laisse moi tranquille..."
        ]
}

PNJ_NAMES = {
    "pnj_1": "Jacob Le Vieux",
    "pnj_2": "Passant",
    "pnj_3": "Passant",
    "pnj_4": "Passant",
    "pnj_5": "Passant",
    "pnj_6": "Essone"
}

# ----------EXEMPLE DE MOB----------
ENEMY_DATA = {
    0: {
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
            "conséquence": None
        }
    },
    1: {
        "name": "Autre Ptit Gus",
        "hp": 30,
        "atq": 6,
        "interaction_options": ["S'informer", "Tirer la langue", "Lui faire une blague"],
        "correct_option_index": 2,
        "description": "C'est juste un enfant...",
        "attacks": {
            "agr": "high",
            "vit": 3,
            "prj": 3,
            "trj": "linear",
            "reb": True,
            "conséquence": None
        }
    },
}

# ----------EXEMPLE DE CARTE----------
# La carte contient des murs "BB", le joueur "XX" et trois PNJ codés "Q1", "Q2" et "Q3".

MAPS_CONFIG = {
    "map1_1": {
        "name": "hub",
        "image": "assets/maps/spawn.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": None,            # pas de map précédente pour la première map
        "next_map": ["map1_2", "map1_5", "map1_6"]   # plusieurs chemins possibles
    },
    "map1_2": {
        "name": "lev_couloir",
        "image": "assets/maps/lev_couloir.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_1",
        "next_map": ["map1_3"]  # fin de parcours ou autre suite
    },
    "map1_3": {
        "name": "lev_main",
        "image": "assets/maps/lev_main.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_2",
        "next_map": ["map1_4"]           # par exemple, un unique chemin vers la suite
    },
    "map1_4": {
        "name": "lev_o1",
        "image": "assets/maps/lev_o1.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_3",
        "next_map": None
    },
    "map1_5": {
        "name": "barrer",
        "image": "assets/maps/barrer.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_1",
        "next_map": ["map1_1"]
    },
    "map1_6": {
        "name": "o1",
        "image": "assets/maps/o1.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_1",
        "next_map": ["map1_7"]
    },
    "map1_7": {
        "name": "o2",
        "image": "assets/maps/o2.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_6",
        "next_map": ["map1_8"]
    },
    "map1_8": {
        "name": "o3",
        "image": "assets/maps/o3.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_7",
        "next_map": ["map1_9", "map1_10"]
    },
    "map1_9": {
        "name": "o3-1",
        "image": "assets/maps/o3-1.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_8",
        "next_map": None
    },
    "map1_10": {
        "name": "o3-2",
        "image": "assets/maps/o3-2.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_8",
        "next_map": None
    },
}
