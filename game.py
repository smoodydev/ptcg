import random

from handle_json import make_card


class Card:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class PokemonCard(Card):
    def __init__(self, name, hp, stage, attacks, weakness, resistance, retreat_cost):
        super().__init__(name)
        self.hp = hp
        self.stage = stage
        self.attacks = attacks

class EnergyCard(Card):
    def __init__(self, name, energy_type):
        super().__init__(name)
        self.energy_type = energy_type

class TrainerCard(Card):
    def __init__(self, name, effect):
        super().__init__(name)
        self.effect = effect



class Deck:
    def __init__(self, cards):
        self.cards = cards


    def draw(self, num_cards):
        if num_cards > len(self.cards):
            return None
        card_index = random.randrange(len(self.cards))
        drawn_card = self.cards.pop(card_index)
        return drawn_card
    
    def remaining(self):
        return len(self.cards)
    





class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.discard = []
        self.hand = []
        self.active = None
        self.bench = []

    def draw(self):
        if len(self.deck.cards) == 0:
            return None
        drawn_card = self.deck.draw(1)
        self.hand.append(drawn_card)
        return drawn_card
    
    def hand_detail(self):
        return [str(card) for card in self.hand]
    
    def tell_hand_detail(self):
        print(self.hand_detail())

    def tell_hand(self):
        print(len(self.hand))

    def tell_deck(self):
        print(self.deck.remaining())

    def has_basic(self):
        pos_cards = make_card(self.hand)
        for id, card in pos_cards.items():
            if card["supertype"] == "Pokemon":
                if card["subtypes"] == "Basic":
                    return True
        return False

    def add_to_bench(self, card):
        if len(self.bench) < 5:
            if isinstance(card, PokemonCard):
                if card.stage == 0:
                    self.bench.append(card)
                    return True
        return False

    def get_state(self):
        object_of = {
            "name": self.name,
            "discard": self.discard,
            "hand": self.hand,
            "active": self.active,
            "bench": self.bench,
            "deck": self.deck.cards

        }
        return object_of





# pikachu = PokemonCard("Pikachu", 60, 0, ["Thunder Shock", "Quick Attack"])

# energy_el = EnergyCard("Electric Energy", "Electric")



# deck1 = [pikachu, pikachu,pikachu,pikachu,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el]
# deck2 = [pikachu, pikachu, pikachu, pikachu, energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el]

# player1 = Player("Stephen", Deck(deck1.copy()))
# player2 = Player("Someone", Deck(deck2.copy()))


def opening_draw(player):
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()


def open_loop(player, deck):
    print(player, deck)
    print(player.name)
    player.deck.cards.extend(player.hand)
    player.hand = []
    opening_draw(player)

def match_opening(player1, player2):
    opening_draw(player1)
    opening_draw(player2)

    
    while not player1.has_basic():
        open_loop(player1, player1.deck)
    
    while not player2.has_basic():
        open_loop(player2, player2.deck)

    print(player1.hand_detail())

    player1.tell_deck()
    player1.tell_hand()

    print(player2.hand_detail())
    player2.tell_deck()
    player2.tell_hand()





def player_select_active(player):
    card_index = int(input("Select Card From Hand - "))
    card = player.hand[card_index-1]
    if isinstance(card, PokemonCard):
        if card.stage == 0:
            player.active = card
            player.hand.pop(card_index)
            return True
    print(str(player.active))
    print(str(player.hand_detail()))
    player_select_active(player)
    

def tell_game_state(player1, player2):
    print("player 1")
    player1.tell_deck()
    player1.tell_hand()
    player1.tell_hand_detail()
    print(str(player1.active))

    print("player 2")
    player2.tell_deck()
    player2.tell_hand()
    player2.tell_hand_detail()
    print(str(player2.active))



# get_game_state

# match_opening()
# player_select_active(player1)
# player_select_active(player2)
# tell_game_state()
# game_loop()


def start_game(playerA, playerB):
    decka = Deck(playerA["deck"])

    playera = Player(playerA["name"], decka)
    deckb = Deck(playerB["deck"])
    playerb = Player(playerB["name"], deckb)
    match_opening(playera, playerb)
    # player_select_active(player1)
    # player_select_active(player2)
    tell_game_state(playera, playerb)
    print(playera.get_state())
    return playera.get_state(), playerb.get_state()


def match_opening_new():
    pass



def draw(player):
    if len(player["deck"]):
        player["hand"].append(player["deck"].pop())


def shuffle(player):
    random.shuffle(player["deck"])


def start_new_game(playerA, playerB):
    return []