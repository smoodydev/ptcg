from pokemon_data import cards

all_cards = {}

pokemon_fields = ["hp", "evolvesFrom", "abilities", "attacks", "weaknesses", "retreatCost"]

def make_cards():
    all_cards = {}
    # print(cards[0]["data"].keys())
    # print(cards[0]["data"])
    # print(" ")
    for c in cards:
        i = c["data"]
        
        card = {
            "name": i["name"],
            "supertype": i["supertype"],
            "id": i["id"],
            "img": i["images"]["small"]
        }
        
        if i["supertype"] == "Pokemon":
            card["subtypes"] = i["subtypes"][0]
            card["types"] = i["types"][0]
            for f in pokemon_fields:
                if f in i:
                    card[f] = i[f]
        
        elif i["supertype"] == "Energy":
            card["subtypes"] = i["subtypes"][0]
            card["rules"] = i.get("rules", None)
        
        else:
            card["rules"] = i["rules"]

        all_cards[i["number"]] = card
    return all_cards
        # if i["number"] == "102":
        #     # print(i)




def make_card(deck):
    all_cards = make_cards()
    card_db = {}
    for card in deck:
        card_db[str(card)] = all_cards[str(card)]
    return card_db


# make_card([97, 34, 98, 8, 28, 46, 47, 92, 81, 52, 93, 24, 26, 91, 60, 61, 94, 95])