// Master class for Card
class Card {
    constructor(name, type, imageUrl) {
        this.name = name;
        this.type = type;
        this.imageUrl = imageUrl;
    }

    // Method to get the card's name
    getName() {
        return this.name;
    }

    // Method to get the card's type
    getType() {
        return this.type;
    }

    // Method to get the card's image URL
    getImageUrl() {
        return this.imageUrl;
    }
}

// Subclass for Pokemon cards
class PokemonCard extends Card {
    constructor(name, type, hp, stage, evolvesFrom, attacks, weakness, resistance, retreatCost, imageUrl) {
        super(name, type, imageUrl);
        this.hp = hp;
        this.stage = stage;
        this.evolvesFrom = evolvesFrom;
        this.attacks = attacks;
        this.weakness = weakness;
        this.resistance = resistance;
        this.retreatCost = retreatCost;
    }

    // Method to get the card's HP
    getHP() {
        return this.hp;
    }

    // Method to get the card's stage
    getStage() {
        return this.stage;
    }

    // Method to get the card's evolution
    getEvolvesFrom() {
        return this.evolvesFrom;
    }

    // Method to get the card's attacks
    getAttacks() {
        return this.attacks;
    }

    // Method to get the card's weakness
    getWeakness() {
        return this.weakness;
    }

    // Method to get the card's resistance
    getResistance() {
        return this.resistance;
    }

    // Method to get the card's retreat cost
    getRetreatCost() {
        return this.retreatCost;
    }
}

// Subclass for Trainer cards
class TrainerCard extends Card {
    constructor(name, type, effect, imageUrl) {
        super(name, type, imageUrl);
        this.effect = effect;
    }

    // Method to get the card's effect
    getEffect() {
        return this.effect;
    }
}

// Subclass for Energy cards
class EnergyCard extends Card {
    constructor(name, type, imageUrl) {
        super(name, type, imageUrl);
    }
}

// Example usage of the card subclasses

// Creating a Pokémon card
const pikachuCard = new PokemonCard(
    'Pikachu',
    'Electric',
    60,
    'Basic',
    '',
    [
        { name: 'Thunder Shock', cost: ['Electric'], damage: 20 },
        { name: 'Quick Attack', cost: ['Colorless', 'Colorless'], damage: 30 },
    ],
    { type: 'Fighting', value: '×2' },
    { type: 'Metal', value: '-20' },
    1,
    'https://example.com/pikachu.jpg'
);

// Creating a Trainer card
const potionCard = new TrainerCard(
    'Potion',
    'Item',
    'Heal 30 damage from one of your Pokémon.',
    'https://example.com/potion.jpg'
);

// Creating an Energy card
const electricEnergyCard = new EnergyCard(
    'Electric Energy',
    'Electric',
    'https://example.com/electric-energy.jpg'
);

// Accessing attributes and methods of the created cards
console.log(pikachuCard.getName()); // Output: Pikachu
console.log(pikachuCard.getType()); // Output: Electric
console.log(pikachuCard.getHP()); // Output: 60
console.log(potionCard.getEffect()); // Output: Heal 30 damage from one of your Pokémon.
console.log(electricEnergyCard.getImageUrl()); // Output: https://example.com/electric-energy.jpg


let playerDeck = [];
let playerHand = [];
let playerBench = [];
let playerDiscard = [];
let opponentDeck = [];
let opponentHand = [];
let opponentDiscard = [];

function createDecks(deck){
    for (let i=0; i < 50; i++){
        deck.push(electricEnergyCard);
    }
    for (let i=0; i < 2; i++){
        deck.push(pikachuCard);
    }
    for (let i=0; i < 8; i++){
        deck.push(potionCard);
    }
    console.log(deck.length);
}

function dealCard(deck, hand){
    if (0 !== -1) {
        let toMove = deck[0];
        deck.splice(0, 1); // Remove the object from array A
        hand.push(toMove); // Add the object to array B
    }
}

Array.prototype.shuffle = function() {
    let m = this.length, i;
    while (m) {
      i = (Math.random() * m--) >>> 0;
      [this[m], this[i]] = [this[i], this[m]]
    }
    return this;
  }

createDecks(playerDeck);
createDecks(opponentDeck);

playerDeck.shuffle()
opponentDeck.shuffle()

for (let i=0; i <7; i++){
    dealCard(playerDeck, playerHand);
}

for (let i=0; i <7; i++){
    dealCard(opponentDeck, opponentHand);
}


function createHand(hand, owner){
    let handDiv = document.getElementById(owner+"-hand");
    hand.forEach((card) => {
        // Create a <div> element
        const div = document.createElement('button');
        
        // Set the text content of the <div> element to the current fruit
        div.textContent = card.name;
        
        // Append the <div> element to the body or a container element
        handDiv.appendChild(div);
      });
}

createHand(playerHand, "player");
createHand(opponentHand, "opponent");

console.log(playerDeck.length, playerHand.length);
console.log(playerDeck, playerHand);

