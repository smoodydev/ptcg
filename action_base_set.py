import random

g_state =[
    {
        'active': {'card': 10, 'dmg': 0, 'energies': ['Psychic','Fire','Water','Water','Water','Water'], 'status': [], 'turn': 0},
        'bench': [{'card': 9, 'dmg': 0, 'energies': ['Grass'], 'status': [], 'turn': 0}], 
        'deck': [98, 52, 61, 98, 52, 47, 28, 97, 92, 97, 47, 97, 98, 46, 24, 97, 81, 97, 52, 46, 91, 94, 98, 98, 60, 98, 97, 97, 8, 60, 60, 93, 98, 97, 97, 47, 98, 97, 97, 98, 97, 26, 60, 61, 46, 97, 98, 98, 34, 24, 97, 34], 
        'discard': [], 
        'hand': [52, 97, 95, 98, 98, 98], 
        'name': 'Starter'
    }, 
    {
        'active': {'card': 60, 'dmg': 0, 'energies': ['Water', 'Water', 'Water', 'Water'], 'status': [], 'turn': 0}, 
        'bench': [{'card': 9, 'dmg': 0, 'energies': ['Water'], 'status': [], 'turn': 0}], 
        'deck': [97, 98, 95, 52, 61, 47, 97, 52, 97, 98, 81, 98, 98, 97, 93, 98, 28, 98, 46, 97, 97, 34, 47, 46, 47, 91, 52, 97, 97, 97, 94, 60, 92, 98, 24, 97, 24, 34, 98, 46, 98, 98, 26, 98, 60, 98, 97, 8, 97, 60, 98, 97, 97], 
        'discard': [], 
        'hand': [98, 46, 61, 97, 98, 52], 
        'name': 'Stephen'
        
    }, 
    1, 
    False
]


# player = game_state[0]
# opponent = game_state[1]



def get_active(player):
    return player["active"]



def do_attack(game_state, attack_id, **kwargs):
    player = game_state[0]
    opponent = game_state[1]
    active = get_active(player)
    try:
        
        attack_steps = cards[active["card"]]["attacks"][attack_id]
        for step in attack_steps:
            step[0](step[1])
    except:
        print("NO CLUE")
    return game_state




cards = {
    1:{
        "name": "Alakazam",
        "power": [
            "damage_swap"
        ],
        "attacks": [
            [
                ("damage", 30),
                ("flip", {1: ("status", "confused", None), 0: None})
            ],

        ]
    },
    2:{
        "name": "Blastoise",
        "power": [
            "Rain_Dance"
        ],
        "attacks": [
            [
                ("damage", 40),
                ("energy_boost", ["Water", 3, 2, 10])
            ],

        ]
    },
    3:{
        "name": "Chansey",
        
        "attacks": [
            [   
                ("flip", {1: ("status", "immune", "self"), 0: None})
            ],
            [
                ("damage", 80),
                ("damage_tar", 80, "self"),
            ],

        ]
    },
    4:{
        "name": "Charizard",
        "power": [
            "Energy_Burn"
        ],
        "attacks": [
            [   
                ("requires_discard", ["Fire", "Fire"]),
                ("damage", 100)
            ]
        ]
    },
    5:{
        "name": "Clefairy",
        "attacks": [
            [   
                ("flip", {1: ("status", "sleep", None), 0: None})
            ],
            [   
                ("NOT IMPLEMENTED"),
            ]
        ]
    },

    6:{
        "name": "Gyarados",
        "attacks": [
            [
                ("damage", 50)
            ],
            [   
                ("damage", 40),
                ("flip", {1: ("status", "paralysed", None), 0: None})
            ]
        ]
    },

    7:{
        "name": "Hitmonchan",
        "attacks": [
            [
                ("damage", 20)
            ],
            [   
                ("damage", 40),
            ]
        ]
    }, 
    8:{
        "name": "Machamp",
        "power": [
            "Strikes_Back"
        ],
        "attacks": [
            [   
                ("damage", 60),
            ]
        ]
    },
    9:{
        "name": "Magneton",
        "attacks": [
            [
                ("damage", 30),
                ("flip", {1: ("status", "paralysed", None), 0: None})
            ],
            [   
                ("damage", 80),
                ("damage_tar", 80, "self"),
                ("damage_all_bench", 20, "player"),
                ("damage_all_bench", 20, "opponent"),
            ]
        ]
    },
    10:{
        "name": "Mewtwo",
        "attacks": [
            [
                ("damage", 10),
                ("damage_extra_for", ["enemy", "energies", 10])
            ],
            [   
                ("requires_discard", ["Psychic"]),
                ("status", "immune", "self")
            ]
        ]
    },

    24:{
        "name": "Charmeleon",
        "attacks": [
            [
                ("damage", 30)
            ],
            [   
                ("requires_discard", ["Fire"]),
                ("damage", 50)
            ]
        ]
    },

    26:{
        "name": "Dratini",
        "attacks": [
            [
                ("damage", 10),
                
            ]
        ]
    },

    27:{
        "name": "Farfetch'd",
        "attacks": [
            [
                ("status", "leek_slap","self"),
                ("damage", 30)
                
            ],
            [
                ("damage", 30),
                
            ]
        ]
    },


    28:{
        "name": "Growlithe",
        "attacks": [
            [
                ("damage", 20),
                
            ]
        ]
    },



    46:{
        "name": "Charmander",
        "attacks": [
            [
                ("damage", 10)
            ],
            [   
                ("requires_discard", ["Fire"]),
                ("damage", 30)
            ]
        ]
    },

    52:{
        "name": "Machop",
        "attacks": [
            [
                ("damage", 20)
            ],
        ]
    }

    ,
    60:{
        "name": "Ponyta",
        "attacks": [
            [
                ("damage", 20)
            ],
            [   
                ("damage", 30)
            ]
        ]
    },
    61: {
        "name": "Rattata",
        "attacks": [
            [
                ("damage", 20)
            ],

        ]
    },

}



# print(do_attack(g_state, 0))



class GameState:
    def __init__(self, session_game_state):
        # Initialize the GameStat object with the game_state from the Flask session
        self.game_state = session_game_state
        self.player = session_game_state[0]
        self.opponent = session_game_state[1]


    def get_active_id(self):
        return self.game_state[0]["active"]["card"]
    
    def get_active(self):
        return cards[self.get_active_id()]
    
    def get_opponent_active(self):
        return cards[self.get_active_id()]

    def update_game_state(self):
        # Function to update the game_state with any changes made during interactions
        # This could involve updating the game_state based on the action and kwargs passed
        pass





    # Handles any dealing of damage that may be required
    def deal_damage(self, dmg, tar=None):
        if tar:
            return
        
        else:
            target = self.opponent["active"]
            print(target)
        if target["status"]:
            print("SHOULD DO STATUS")
        
        target["dmg"] = target["dmg"] + dmg
        print(target)


    def deal_damage_target(self, dmg, target):
        print(target)
        print(target["dmg"])
        target["dmg"] = target["dmg"] + dmg
        print(target["dmg"])


    # Handle any energy discarding that may be required
    def discard_energys(self, energies, tar=None):
        if tar:
            pass
        else:
            card = self.game_state[0]["active"]
            for e in energies:
                card["energies"].remove(e)
            
    

    def apply_status(self, status, tar=None):
        if tar:
            print()
            if tar == "self":
                target = self.player["active"]
            print("HELP ME")
        else:
            target = self.opponent["active"]
        target.get("status", [])
        target["status"].append(status)
        print(target["status"])




    def do_flip(self, results):
        # print(results)
        flip = random.randint(0, 1)
        if flip:
            effect = (results[0])
        else:
            effect = results[1]
        if effect:
            if effect[0] == "status":
                effect[0] 
                self.apply_status(effect[1], effect[2])
    
    def energy_boost(self, details):
        energy_count = self.player["active"]["energies"].count(details[0])
        extra_energies = energy_count - details[1]
        dmg = extra_energies * details[3]
        if dmg >= 0 :
            if dmg > details[2] * details[3]:
                dmg = details[2] * details[3]
            self.deal_damage(dmg)

        else:
            print("NO EXTRA DAMAGE")
    
    def damage_extra_for(self, details):
        if details[0] == "enemy":
            target = self.opponent["active"]
        
        if details[1] == "energies":
            counted = len(target["energies"])
        else:
            counted = 0
        target["dmg"] = target["dmg"] + (counted * details[2])

    def get_target(self, tar_text):
        if tar_text == "self":
            target = self.player["active"]
            print(target)
            return target






    def handle_attack(self, a_id, **kwargs):
        data = self.get_active()
        attack_steps = data["attacks"][a_id]
        # try:
        for step in attack_steps:
            print(step)
            if step[0] == "damage":
                self.deal_damage(step[1])
            elif step[0] =="damage_tar":
                target = self.get_target(step[2])
                print(target)
                print("YA HOOO")
                self.deal_damage_target(step[1], target)
            elif step[0] =="damage_all_bench":
                if step[2] == "player":
                    for b in self.player["bench"]:
                        self.deal_damage_target(step[1], b)
                else:
                    for b in self.opponent["bench"]:
                        self.deal_damage_target(step[1], b)
            elif step[0] == "status":
                self.apply_status(step[1], step[2])
            elif step[0] == "requires_discard":
                self.discard_energys(step[1])
            elif step[0] == "flip":
                self.do_flip(step[1])
            elif step[0] == "energy_boost":
                self.energy_boost(step[1])
            elif step[0] == "damage_extra_for":
                self.damage_extra_for(step[1])
            else:
                raise Exception
                return True
        # except Exception as e:
            # print("NOPE")
            # print(e)
            # return False
        
        # print(**kwargs)
        pass

    def tell_game_state(self):
        return self.game_state
    

# game_state = GameState(g_state)

# game_state.handle_attack(0)
# game_state.handle_attack(1)

# print(game_state.game_state)

starter_deck = [
    47, 47, 47,        # diglett
    52, 52, 52, 52,     # machop
    34, 34,             #Machoke
    8, #Machamp
    60, 60, 60, 60, # ponyta
    46, 46, 46, 46, # Charmander
    24, 24,  # Charmeleon
    28, #growlithe
    61, 61, # Rattata
    26, # Dratini
    #97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, #fighting
    #98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, #fire
    #81, 91, 92, 93, 94, 95 # trainers 
]



# def check_ids_exist(req_cards):
#     exists = set()
#     missing = set()
#     for c in req_cards:
#         if c in cards:
#             exists.add(c)
#         else:
#             missing.add(c)
#     return [exists, missing]

# check = check_ids_exist(starter_deck)
# print(check)
