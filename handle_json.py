from pokemon_data import cards

all_cards = {}

pokemon_fields = ["hp", "evolvesFrom", "abilities", "attacks", "weaknesses", "retreatCost"]

def make_cards():
    print(cards[0]["data"].keys())
    print(cards[0]["data"])
    print(" ")
    for c in cards:
        i = c["data"]
        
        card = {
            "name": i["name"],
            "supertype": i["supertype"],
            "id": i["id"]
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
        # if i["number"] == "102":
        #     # print(i)
    print(all_cards["1"])
    print(all_cards["85"])
    print(all_cards["102"])



def make_card(deck)
    all_cards = make_cards()
    deck_back
    for card in deck:
        pass



# make_cards()