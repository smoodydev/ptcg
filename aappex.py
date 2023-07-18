import random

class Card:
    def __init__(self, name):
        self.name = name

class PokemonCard(Card):
    def __init__(self, name, hp, attacks):
        super().__init__(name)
        self.hp = hp
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
        drawn_cards = random.sample(self.cards, num_cards)
        self.cards = [card for card in self.cards if card not in drawn_cards]
        return drawn_cards

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.field = []

    def draw_initial_cards(self, num_cards):
        self.hand = self.deck.draw(num_cards)
        if not self.has_pokemon_card():
            self.deck.cards.extend(self.hand)
            self.hand = []
            self.draw_initial_cards(num_cards)

    def has_pokemon_card(self):
        for card in self.hand:
            if isinstance(card, PokemonCard):
                return True
        return False

    def set_pokemon_card(self, card_index):
        pokemon_card = self.hand[card_index]
        if isinstance(pokemon_card, PokemonCard):
            self.field.append(pokemon_card)
            del self.hand[card_index]

# Example usage
pokemon_card1 = PokemonCard("Pikachu", 60, ["Thunder Shock", "Quick Attack"])
pokemon_card2 = PokemonCard("Charizard", 120, ["Flamethrower", "Wing Attack"])
energy_card = EnergyCard("Fire Energy", "Fire")
trainer_card = TrainerCard("Potion", "Heal 30 HP")

cards = [pokemon_card1, pokemon_card2, energy_card, trainer_card, pokemon_card1, pokemon_card2, energy_card, trainer_card, pokemon_card1, pokemon_card2, energy_card, trainer_card]
deck = Deck(cards)

player1 = Player("Player 1", deck)
player1.draw_initial_cards(7)

# Prompt player 1 to set a Pokemon card onto the field
print(f"{player1.name}'s Hand: {', '.join(card.name for card in player1.hand)}")
while not player1.field:
    card_index = int(input(f"{player1.name}, select a Pokemon card from your hand to set onto the field (enter the card index): "))
    player1.set_pokemon_card(card_index)


deck2 = Deck(cards)
player2 = Player("Player 2", deck2)
print([card.name for card in player2.deck.cards])
player2.draw_initial_cards(7)

# Prompt player 2 to set a Pokemon card onto the field
print(f"{player2.name}'s Hand: {', '.join(card.name for card in player2.hand)}")
while not player2.field:
    card_index = int(input(f"{player2.name}, select a Pokemon card from your hand to set onto the field (enter the card index): "))
    player2.set_pokemon_card(card_index)

# Print the hands and fields of both players
print(f"{player1.name}'s Hand: {', '.join(card.name for card in player1.hand)}")
print(f"{player1.name}'s Field: {', '.join(card.name for card in player1.field)}")
print(f"{player2.name}'s Hand: {', '.join(card.name for card in player2.hand)}")
print(f"{player2.name}'s Field: {', '.join(card.name for card in player2.field)}")