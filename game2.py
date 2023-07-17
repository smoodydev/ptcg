import random

class Card:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class PokemonCard(Card):
    def __init__(self, name, hp, stage, attacks):
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
        print(self.name)
        for card in self.hand:
            print("Check")
            if isinstance(card, PokemonCard):
                if card.stage == 0:
                    return True
        return False

    def add_to_bench(self, card):
        if len(self.bench) < 5:
            if isinstance(card, PokemonCard):
                if card.stage == 0:
                    self.bench.append(card)
                    return True
        return False





pikachu = PokemonCard("Pikachu", 60, 0, ["Thunder Shock", "Quick Attack"])

energy_el = EnergyCard("Electric Energy", "Electric")



deck1 = [pikachu, pikachu,pikachu,pikachu,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el]
deck2 = [pikachu, pikachu, pikachu, pikachu, energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el,energy_el]

player1 = Player("Stephen", Deck(deck1.copy()))
player2 = Player("Someone", Deck(deck2.copy()))


def opening_draw(player):
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()


def open_loop(player, deck):
    print(player.name)
    player.hand = []
    player.deck = Deck(deck.copy())
    opening_draw(player)

def match_opening():
    opening_draw(player1)
    opening_draw(player2)

    while not player1.has_basic():
        open_loop(player1, deck1)
    
    while not player2.has_basic():
        open_loop(player2, deck2)

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
    

def tell_game_state():
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


# match_opening()
# player_select_active(player1)
# player_select_active(player2)
# tell_game_state()
# game_loop()


def start_game():
    match_opening()
    player_select_active(player1)
    player_select_active(player2)
    tell_game_state()