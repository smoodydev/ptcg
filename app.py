import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session, send_file, url_for
from flask_pymongo import PyMongo, ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

from base_set import base_set_cards
from game import start_game, draw, shuffle
from handle_json import make_card
from action_base_set import GameState

import json
import functools
import random

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# app.config["MONGO_DBNAME"] = os.environ.get('DATABASE')

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRETKEY", "SomeSecret")

mongo = PyMongo(app)
app.templates = ""


def login_required(func):
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if "player_name" not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper_login_required


@app.template_filter('dictsort_custom')
def dictsort_custom(d):
    return sorted(d.items(), key=lambda x: int(x[0]))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage-cards")
@login_required
def manage_cards():
    return render_template("mange_cards.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route('/register', methods=['POST'])
def register():
    player_name = request.form['playerName']
    email = request.form['email']
    password = request.form['password']

    # Check if a player with the same name or email already exists
    existing_player = mongo.db.players.find_one({"$or": [{"player_name": player_name}, {"email": email}]})

    if existing_player:
        return "Player with the same name or email already exists."

    registration_data = {
        'player_name': player_name,
        'email': email,
        'password': generate_password_hash(password)
    }

    # Save registration data to MongoDB
    mongo.db.players.insert_one(registration_data)
    session["player_name"] = player_name

    return "Registration successful!"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        player_name = request.form['loginPlayerName']
        password = request.form['loginPassword']

        # Check if a player record with the given name exists
        player = mongo.db.players.find_one({"player_name": player_name})

        if player:
            # Verify password
            if check_password_hash(player['password'], password):
                # Password matches, login successful
                # You can store player details in the session if needed
                session["player_name"] = player_name
                return redirect(url_for('profile'))
        
        # Player record not found or password does not match
        return "Invalid player name or password."

    else:
        return redirect(url_for('signin'))







@app.route('/profile')
@login_required
def profile():
    # Access the logged-in user's name from the session
    player_name = session.get('player_name')
    player = mongo.db.players.find_one({"player_name": player_name})
    mongo.db.players.update_one({'player_name': player_name}, {'$set': {'credits': 100}})
    return render_template('profile.html', player=player, deck=get_deck())





@app.route('/profile/change_password', methods=['POST'])
@login_required
def change_password():
    player_name = session.get('player_name')

    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']

    # Retrieve the player record from the database
    player = mongo.db.players.find_one({"player_name": player_name})

    if player and check_password_hash(player['password'], current_password):
        # Current password matches, hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the player's password in the database
        mongo.db.players.update_one({"player_name": player_name}, {"$set": {"password": hashed_password}})

        return "Password changed successfully!"
    else:
        return "Invalid current password."






@app.route('/logout')
@login_required
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login'))



grass_deck = [15, 30, 30, 44, 44, 44, 44, 45, 45, 54, 54, 54, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
fire_deck = [3, 24, 24, 46, 46, 46, 46, 23, 23, 28, 28, 28, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98]
water_deck = [2, 42, 42, 63, 63, 63, 63, 38, 38, 59, 59, 59, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102]


start_trainers = [81, 91, 92, 92, 94, 95]


evo_test = [
         
    52, 52, 52, 52, 52, 52, 52, 52,     # machop
    34, 34, 34, 34, 34, 34, 34, 34,            #Machoke

    46, 46, 46, 46, # Charmander
    24, 24, 24, 24,  # Charmeleon
    97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97

]




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
    97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, #fighting
    98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, #fire
    81, 91, 92, 93, 94, 95 # trainers 
]

starter_deck2 = [
    2, #Blastoise
    42, 42, #wart
    63, 63, 63, 63, #squritle

    38, 38, # poliwril 
    59, 59, 59,       # poliwag
    
    60, 60, 60, 60, # ponyta
    46, 46, 46, 46, # Charmander
    24, 24,  # Charmeleon
    28, #growlithe
    
    26, # Dratini
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, #fighting
    98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, #fire
    81, 91, 92, 93, 94, 95 # trainers 
]

"""
3×	Diglett	Fighting	Common
4×	Machop	Fighting	Common
2×	Machoke	Fighting	Uncommon
1×	Machamp	Fighting	Rare Holo
4×	Ponyta	Fire	Common
4×	Charmander	Fire	Common
2×	Charmeleon	Fire	Uncommon
1×	Growlithe	Fire	Uncommon
2×	Rattata	Colorless	Common
1×	Dratini	Colorless	Uncommon
1×	Bill	T	Common
1×	Energy Removal	T	Common
1×	Energy Retrieval	T	Uncommon
1×	Gust of Wind	T	Common
1×	Pokédex	T	Uncommon
2×	Potion	T	Common
2×	Switch	T	Common
14×	Fighting Energy	Fighting E	—
14×	Fire Energy
"""

@app.route('/select_option', methods=["GET", "POST"])
@login_required
def select_option():
    print(len(starter_deck) + len(start_trainers))
    if request.method == "POST":
        if "coin" not in session:
            if request.form["option"] == "grass":
                print(len(grass_deck) + len(start_trainers)*2)
            elif request.form["option"] == "fire":
                print(len(fire_deck))
            elif request.form["option"] == "water":
                print(len(water_deck))
            
    # Access the logged-in user's name from the session
    player_name = session.get('player_name')

    return render_template('options.html')



@app.route('/collection')
@login_required
def collection():
    # Access the logged-in user's name from the session
    player_name = session.get('player_name')
    player = mongo.db.players.find_one({"player_name": player_name})

    # add_cards_to_collection(player["_id"], ["1","2","3","4"])
    player = mongo.db.players.find_one({"player_name": player_name})
    cards = base_set_cards
    return render_template('collection.html', player=player, cards=cards)




@app.route('/card_shop', methods=["GET", "POST"])
@login_required
def card_shop():
    packs = {
        1:{"name":"Base Set", "description": "1 Rare, 3 Uncommon, 6, Common, 1 Energy Card", "code": "base_booster", "cost": 50}, 
        2:{"name":"Base Set (3)", "description": "1 Rare, 1 Uncommon, 1 Common", "code": "base_booster2", "cost": 35}, 
        3:{"name":"Base Set (Limited)", "description": "2 Rare, 5 Uncommon, 13 Common, 5 Energy", "code": "base_booster3", "cost": 110}
        }
    if request.method == "POST":
        player_name = session.get('player_name')
        player = mongo.db.players.find_one({"player_name": player_name})
        if player["credits"]:
            pack_id = request.form.get("pack_id", None)
            print(pack_id)
            req_pack = packs[int(pack_id)]
            if req_pack["cost"] <= player["credits"]:
                cards = generate_pack_cards(req_pack)
                print(cards)
                add_cards_to_collection(player["_id"], cards)
                return cards
    player_name = session.get('player_name')
    player = mongo.db.players.find_one({"player_name": player_name})
    packs = {1:{"name":"Base Set", "description": "1 Rare, 3 Uncommon, 6, Common, 1 Energy Card", "code": "base_booster"}, 2:{"name":"Base Set (3)", "description": "1 Rare, 1 Uncommon, 1 Common", "code": "base_booster2"}, 3:{"name":"Base Set (Limited)", "description": "1 Rare, 4 Uncommon, 10 Common, 5 Energy", "code": "base_booster3"}}
    return render_template('card_shop.html', player=player, packs=packs)


def get_deck():
    if "deck" not in session:
        a_set = base_set_cards
        starter_deck.sort()
        deck = [a_set[card] for card in starter_deck]
        print(len(deck))
        count = {}
        for num in deck:
            if num in count:
                count[num] += 1
            else:
                count[num] = 1
        print(count)
        return count




# HERE

@app.route('/play/find', methods=["GET", "POST"])
@login_required
def play_find():
    player_name = session["player_name"]
    if request.method == "POST":
        data = request.form
        if data.get("rType", "") == "accept":
            
            invite_id = data.get("opponentName")
            
            game = mongo.db.match_invite.find_one({"_id": ObjectId(invite_id)})
            if game:
                # FIX:  Will TESTING PURPOSES ONLY CURRENTLY
                invited = mongo.db.players.find_one({"player_name": player_name})
                inviter = mongo.db.players.find_one({"player_name": game["inviter"]})


                flip = random.randint(0, 1)


                enemy = {"name": "Bad Player", "deck": starter_deck.copy()}
                if flip:
                    print("Heads - Inviter Goes First")
                    opponent, player = start_game(enemy, {"name": player_name, "deck": starter_deck.copy()})
                    
                    game_state = [opponent, player, 0]

                    match_data = {
                        "player_one": game["inviter"],
                        "player_two": player_name,
                        "game_state": game_state
                    }
                else:
                    print("Tails - Invited Goes First")
                    player, opponent = start_game({"name": player_name, "deck": starter_deck.copy()}, enemy)
                    
                    game_state = [player, opponent, 0]

                    match_data = {
                        "player_one": player_name,
                        "player_two": game["inviter"],
                        "game_state": game_state
                    }

                # print(match_data)

                # a, b = mongo.db.match.insert_one(match_id=match_data)
                # print(a, b)
                # return redirect(url_for("play_match", b))

                cards_req = list(set(starter_deck.copy() + starter_deck.copy()))

                card_db = make_card(cards_req)
                player_game_state = get_player_state(game_state, player_name)
                return render_template("match.html", game=json.dumps(player_game_state), turn = game_state[2], card_db=json.dumps(card_db))
            else:
                print(list(mongo.db.match_invite.find()))
        elif data.get("rType", "") == "invite":
            opponent_name = data.get("opponentName")
            if opponent_name:
                match_data = {"inviter": player_name, "invited": opponent_name}
                print(match_data)
                mongo.db.match_invite.insert_one({"inviter": player_name, "invited": opponent_name})

    match_invites = mongo.db.match_invite.find({"inviter": player_name})
    match_invited = mongo.db.match_invite.find({"invited": player_name})
    return render_template("find_match.html", match_invites=match_invites, match_invited=list(match_invited))







@app.route('/play/<match_id>', methods=["GET", "POST"])
@login_required
def play_match(match_id):
    match = mongo.db.match.find_one(match_id=match_id)
    if match:
        if match["player1"] == session["player_name"]:
            return match
    return redirect(url_for('profile'))










@app.route('/practice/', methods=["GET", "POST"])
@login_required
def practice():
    npc_choices = [{"name": "Starter", "id": "starter"}]

    return render_template("pick_practice.html", npcs=npc_choices)

@app.route('/clearpractice/')
@login_required
def clearpractice():
    del session["npc"]
    return redirect(url_for('practice'))


@app.route('/practice/<npc>')
@login_required
def practice_npc(npc):
    
    """
    Handles Starting a new game.
    """
    cards_req = list(set(starter_deck.copy() + starter_deck.copy()))
    print(starter_deck.copy())
    print(cards_req)
    print(cards_req)
    card_db = make_card(cards_req)
    if "npc" not in session:
        print(npc)
        npc_choices = {
            "starter": {
                "name": "Starter",
                "deck": starter_deck.copy()
            }
        }

        enemy = npc_choices[npc]
        
        player, npc = start_game({"name": "Stephen", "deck": starter_deck.copy()}, enemy)

        turn = 0
        energy = False

        shuffle(player)
        shuffle(npc)
        game_state = [player, npc, turn, energy, 1]
        session["npc"] = game_state
    else:
        game_state = session["npc"]
        player = game_state[0]
        npc = game_state[1]


    print(game_state)
    return render_template("match.html", game=json.dumps(game_state), turn = game_state[2], card_db=json.dumps(card_db))


@app.route('/match/npc', methods=["POST"])
@login_required
def perform_action():
    game_state = session.get("npc")
    
    if not game_state or not isinstance(game_state, list) or len(game_state) < 3:
        return jsonify({"v": False, "message": "Invalid game state"}), 400

    player, opponent, turn, energy, player1 = game_state


    if turn != 0 and turn % 2 != player1:
        return jsonify({"v": False, "message": "Invalid game state"}), 400

    data = request.get_json().get("data")

    fail_response = {"v": False, "message": "Could not play this card"}
    valid_response = {"v": 1, "message": "Card Played"}
    requires_energies = {"v": 2, "message": "Requires Energies"}
    aavalid_response = {"v": 3, "message": "Card Played"}
    aavalid_response = {"v": 4, "message": "Card Played"}
    aavalid_response = {"v": 5, "message": "Card Played"}
    


    if data["turn"] == turn:
        action_type = data["type"]
    
        # --------------------------------------------------------------
        # ---   HAND ACTION - Set Pokemon, Evolve, Trainer, Energy   ---
        # --------------------------------------------------------------
        if action_type == "hand":
            index = data["card_index"]        
            #    -----------------   Playing Pokemon Cards   -----------------
            if data["card"]["supertype"] == "Pokemon":
                if data["card"]["subtypes"] == "Basic":
                    if turn == 0 and player["active"] == None:
                        player["active"] = {"card": player["hand"].pop(index), "dmg": 0, "energies":[], "status": None, "turn": turn}
                    elif len(player["bench"]) < 5:
                        player["bench"].append({"card": player["hand"].pop(index), "dmg": 0, "energies":[], "status": None, "turn": turn})
                    else:
                        return jsonify(fail_response), 200
                    session["npc"][0] = player
                    session["npc"] = session["npc"]
                    
                    return jsonify(valid_response), 200

                elif data["card"]["subtypes"] != "Basic":
                    target = data["target"].split("-")
                    if target[1] == "player":
                        evo_form = data["card"]['evolvesFrom']
                        if target[0] == "active":
                            if turn != player["active"]["turn"]:
                                p_card = player["active"]["card"]
                                card_db = make_card([p_card])

                                if card_db[str(p_card)]["name"] == evo_form:
                                    player["active"]["card"] = player["hand"].pop(index)
                                    player["active"]["turn"] = turn
                                    
                                    session["npc"] = session["npc"]
                                    return jsonify(valid_response), 200
                                return jsonify(fail_response), 200
                        elif target[0] == "bench":

                            pk_tar = player["bench"][int(target[2])]
                            if turn != pk_tar["turn"]:

                                p_card = pk_tar["card"]
                                card_db = make_card([p_card])
                                
                                if card_db[str(p_card)]["name"] == evo_form:
                                    pk_tar["card"] = player["hand"].pop(index)
                                    pk_tar["turn"] = turn
                                    
                                    session["npc"] = session["npc"]
                                    return jsonify(valid_response), 200

            #    -----------------   ENERGY ATTACHEMENT   -----------------
            elif data["card"]["supertype"] == "Energy":
                if energy:
                    tar = data["target"].split("-")
                    if tar[1] == "player":
                        if tar[0] == "bench":
                            player[tar[0]][int(tar[2])]["energies"].append(data["card"]["name"].split(" ")[0])
                        else:
                            player[tar[0]]["energies"].append(data["card"]["name"].split(" ")[0])
                        
                        player["hand"].pop(index)
                        session["npc"][0] = player
                        session["npc"][3] = False
                        session["npc"] = session["npc"]
                        return jsonify(valid_response), 200

            elif data["card"]["supertype"] == "Trainer":
                print("Trainer")
                print(data["target"])
                print("Not Implemented Yet")
                return jsonify(fail_response), 200

            else:
                print("NOTHING FOUND")
                return jsonify(fail_response), 200
            
            return jsonify(fail_response), 200


        
        elif action_type == "attack":
            g_state = GameState(game_state)
            print(g_state.tell_game_state())
            print("data")
            print(data)
            try:
                g_state.handle_attack(data["attackId"])
                session["npc"] = g_state.tell_game_state()
            except:
                print("SOMETHING WRONG")
            print(g_state.tell_game_state())
            # print(data)
            print("ATTACK")

        elif action_type == "retreat":
            tar = data["target"].split("-")

            target_index = int(tar[2])
            if tar[1] == "player":
                if tar[0] == "bench":
                    if player["bench"][target_index]:
                        energies = player["active"]["energies"]
                        card_db = make_card([player["active"]["card"]])
                        active_card = card_db[str(player["active"]["card"])]
                        if "cost" in data or "retreatCost" not in active_card:
                            cost = data.get("cost", [])

                            if len(energies) >= len(active_card.get("retreatCost", [])):

                                if len(cost) >= len(active_card.get("retreatCost", [])):
                                    try:
                                        for e in cost:
                                            energies.remove(e)
                                    except:
                                        return jsonify(fail_response), 200
                                    
                                    player["active"]["energies"] = energies
                                    temp = player["active"]
                                    player["active"] = player["bench"][target_index]
                                    player["bench"][target_index] = temp
                                    session["npc"][0] = player
                                    
                                    session["npc"] = session["npc"]
                                    return jsonify(valid_response), 200
                            return jsonify(fail_response), 200
                        else:
                            # print(card_db)
                            # print(player["active"])
                            # print(card_db[str(player["active"]["card"])])
                            
                            print(active_card)
                            print(active_card)
                            print(active_card)
                            return_response = requires_energies
                            return_response["energies"] = active_card["retreatCost"]
                            return_response["origin"] = data
                            return_response["options"] = player["active"]["energies"]
                            print(requires_energies)
                            return jsonify(requires_energies), 200
        
        
        elif action_type == "endTurn":
            session["npc"][2] = turn + 1
            session["npc"][3] = True

            if turn ==0:
                print(session["npc"][1])
                opponent = session["npc"][1]
                hand = opponent["hand"]
                card_db = make_card(hand)
                for index, item in enumerate(hand):
                    
                    if card_db[str(item)]["supertype"] =="Pokemon":
                        if card_db[str(item)]["subtypes"] == "Basic":
                            opponent["active"] = {"card": opponent["hand"].pop(index), "dmg": 0, "energies":[], "status": [], "turn": turn}


            temp = session["npc"][0]
            session["npc"][0] = session["npc"][1]
            session["npc"][1] = temp
            print(session["npc"][0])
            draw(session["npc"][0])
            print(session["npc"][0])


            session["npc"] = session["npc"]



            print("END TURN")
            return jsonify(valid_response), 200
        
        
        
        
        else:
            return 500

    print(session["npc"])
    return "Hello"


# @app.route
# @app.route('/practice/<match_id>', methods=["GET", "POST"])
# def practice_match(match_id):
#     match = mongo.db.npc_match.find_one(match_id=match_id)
#     if match:
#         return match
#     return redirect(url_for('profile'))



# HERE
def get_player_state(game_state, player_name):
    print(game_state)
    print(player_name)
    if player_name != game_state[0]["name"]:
        player_temp = game_state[1]
        game_state[1] =  game_state[0]
        game_state[0] = player_temp

    player = game_state[0]
    opponent = game_state[1]
    player["deck"] = ["card" for card in player["deck"]]
    opponent["hand"] = ["card" for card in opponent["hand"]]
    opponent["deck"] = ["card" for card in opponent["deck"]]
    print(game_state)
    return game_state






def generate_pack_cards(x):
    packs = {
        "base_booster" : {
            "set": "base_set",
            "rare": 1,
            "uncommon": 3,
            "common": 6,
            "energy": 1
            }
        }
    pack = packs[x["code"]]
    cards = []
    if pack["set"] == "base_set":
        for i in range(pack["rare"]):
            cards.append(random.randint(1, 16))
        for i in range(pack["uncommon"]):
            cards.append(random.randint(17, 43))
        for i in range(pack["common"]):
            cards.append(random.randint(43, 96))
        for i in range(pack["energy"]):
            cards.append(random.randint(97, 102))
    return cards



def add_cards_to_collection(player_id, card_ids):
    # Assuming you have a MongoDB client and appropriate collections set up
    player_collection = mongo.db['players']
    
    # Fetch the player document
    player = player_collection.find_one({'_id': player_id})
    if player is None:
        print("Player not found!")
        return
    
    # Get the existing collected cards dictionary or initialize it if it doesn't exist
    collected_cards = player.get('collectedCards', {})
    
    # Add 4 copies of each card ID to the collected cards dictionary
    for card_id in card_ids:
        c = str(card_id)
        collected_cards[c] = collected_cards.get(c, 0) + 1
    
    # Update the player document with the modified collected cards dictionary
    print(player_collection.find_one({'_id': player_id}))
    player_collection.update_one({'_id': player_id}, {'$set': {'collectedCards': collected_cards}})
    






if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)