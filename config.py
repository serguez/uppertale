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
        "Hum... Ton silence est ravissant haha",
        "Il y a un bouton je crois en haut à gauche du parc, il ouvre le portail pour aller dans l'école. ",
        "Au revoir"
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
        "Laisse moi tranquille...",
        "...",
        "Tu n'est pas possible.",
        "Ca fait un bon mois que tu n'est pas venu à l'école",
        "Je me suis ramené près de chez toi du coup...",
        "Tu es sur que tu veux pas sortir, même un coup ?"
        "On va pas loin... Juste un peu marcher"
        "...",
        "D'acc... Pas de soucis, prends soin de toi quand même..."
        ],
    "pnj_7":[
        "Oh ?",
        "Ils ont laissé un robot entrer ?",
        "Mh...",
        "J'aime pas les foules",
        "Du coup je me suis caché ici",
        "...",
        "....",
        ".....",
        "......",
        "......."
        "........"
        "...",
        "Bon",
        "Salut ^^"
        ],
    "pnj_8":[
        "Je travaille là..."
        ],
    "pnj_9":[
        "Jeune Robot,tu n'as rien à faire ici."
        ],
    "pnj_10":[
        "Je fais la queue là..."
        ]
}

PNJ_NAMES = {
    "pnj_1": "Jacob Le Vieux",
    "pnj_2": "Passant",
    "pnj_3": "Passant",
    "pnj_4": "Passant",
    "pnj_5": "Passant",
    "pnj_6": "Essone",
    "pnj_7": "Ikari",
    "pnj_8": "Elève un peu trop random",
    "pnj_9": "Madame Pavoshko",
    "pnj_10": "Elève un peu trop random"
}

# ----------EXEMPLE DE MOB----------
ENEMY_DATA = {
    0: {
        "name": "Ptigus",
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
        },
        "has_been_killed": False,
    },
    1: {
        "name": "Gaillard Jr.",
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
        },
        "has_been_killed": False,
    },
    2: {
        "name": "Salgoss",
        "hp": 20,
        "atq": 2,
        "interaction_options": ["S'informer", "Lui faire peur", "Faire des grimaces"],
        "correct_option_index": 2,
        "description": "C'est juste un enfant...",
        "attacks": {
            "agr": "small",
            "vit": 7,
            "prj": 4,
            "trj": "zigzag",
            "reb": False,
            "conséquence": None
        },
        "has_been_killed": False,
    },
    3: {
        "name": "LeKid (mini-boss)",
        "hp": 50,
        "atq": 8,
        "interaction_options": ["S'informer", "Parler de roblox", "Crier"],
        "correct_option_index": 1,
        "description": "C'est juste un enfant...",
        "attacks": {
            "agr": "mid",
            "vit": 2,
            "prj": 6,
            "trj": "sinus",
            "reb": False,
            "conséquence": None
        },
        "has_been_killed": False,
    },
    4: {
        "name": "Le Proviseur",
        "hp": 150,
        "atq": 9,
        "interaction_options": ["S'informer", "Expliquer ce qu'il se passe", "Ne rien dire"],
        "correct_option_index": 1,
        "description": "C'est le proviseur. Les robots ne sont pas autorisés dans l'établissement",
        "attacks": {
            "agr": "high",
            "vit": 4,
            "prj": 6,
            "trj": "linear",
            "reb": True,
            "conséquence": "loadmap1_12"
        },
        "has_been_killed": False,
    },
    5: {
        "name": "Elève pas si random que ça",
        "hp": 60,
        "atq": 3,
        "interaction_options": ["S'informer", "Mépriser", "Donner les réponses"],
        "correct_option_index": 2,
        "description": "C'est un élève. Il a des plavons en crypto à ce qu'il parait",
        "attacks": {
            "agr": "small",
            "vit": 6,
            "prj": 3,
            "trj": "zigzag",
            "reb": True,
            "conséquence": "opendoor_1"
        },
        "has_been_killed": False,
    },
    6: {
        "name": "Dame de la cantine",
        "hp": 75,
        "atq": 4,
        "interaction_options": ["S'informer", "Prendre 2 portions", "Nettoyer la table"],
        "correct_option_index": 2,
        "description": "Clililili :3",
        "attacks": {
            "agr": "high",
            "vit": 2,
            "prj": 10,
            "trj": "sinus",
            "reb": False,
            "conséquence": "opendoor_2"
        },
        "has_been_killed": False,
    },
    7: {
        "name": "Dominique la bibliothéquère",
        "hp": 75,
        "atq": 1,
        "interaction_options": ["S'informer", "Parler très fort", "Lire un livre"],
        "correct_option_index": 2,
        "description": "Dominique DETESTE le bruit",
        "attacks": {
            "agr": "small",
            "vit": 7,
            "prj": 4,
            "trj": "round7",
            "reb": False,
            "conséquence": "opendoor_3"
        },
        "has_been_killed": False,
    },
    8: {
        "name": "Essone",
        "hp": 1,
        "atq": 0,
        "interaction_options": ["S'informer", "Parler très fort", "Lire un livre"],
        "correct_option_index": 2,
        "description": "Dominique DETESTE le bruit",
        "attacks": {
            "agr": "small",
            "vit": 0,
            "prj": 0,
            "trj": "round7",
            "reb": False,
            "conséquence": None
        },
        "has_been_killed": False,
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
        "next_map": ["map1_11"]
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
    "map1_11": {
        "name": "boss_act1",
        "image": "assets/maps/boss_act1.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": None,
        "next_map": None
    },
    #---------------------------Acte 2
    "map1_12": {
        "name": "hall",
        "image": "assets/maps/hall.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": None,
        "next_map": ["map1_13", "map1_14", "map1_15", "map1_16", "map1_17"]
    },
    "map1_13": {
        "name": "rangement",
        "image": "assets/maps/rangement.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_12",
        "next_map": None
    },
    "map1_14": {
        "name": "class1",
        "image": "assets/maps/class1.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_12",
        "next_map": None
    },
    "map1_15": {
        "name": "cantine",
        "image": "assets/maps/cantine.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_12",
        "next_map": None
    },
    "map1_16": {
        "name": "bibliothèque",
        "image": "assets/maps/biblio.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_12",
        "next_map": None
    },
    "map1_17": {
        "name": "final act2",
        "image": "assets/maps/final_act2.png",
        "background": "assets/maps_bg/spawn.png",
        "previous_map": "map1_12",
        "next_map": ["map1_1"]
    },
}
