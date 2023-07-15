import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session, send_file, url_for
from flask_pymongo import PyMongo, ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

from base_set import base_set_cards

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# app.config["MONGO_DBNAME"] = os.environ.get('DATABASE')

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRETKEY", "SomeSecret")

mongo = PyMongo(app)
app.templates = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage-cards")
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
                # You can store player details in the session here if needed
                session["player_name"] = player_name
                return redirect(url_for('profile'))
        
        # Player record not found or password does not match
        return "Invalid player name or password."

    else:
        return redirect(url_for('signin'))







@app.route('/profile')
def profile():
    # Access the logged-in user's name from the session
    player_name = session.get('player_name')

    # If the user is not logged in, redirect to the login page
    if not player_name:
        return redirect(url_for('login'))

    return render_template('profile.html', player_name=player_name, deck=get_deck())

@app.route('/profile/change_password', methods=['POST'])
def change_password():
    player_name = session.get('player_name')

    if not player_name:
        return redirect(url_for('login'))

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
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login'))



grass_deck = [15, 30, 30, 44, 44, 44, 44, 45, 45, 54, 54, 54, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
fire_deck = [3, 24, 24, 46, 46, 46, 46, 23, 23, 28, 28, 28, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98]
water_deck = [2, 42, 42, 63, 63, 63, 63, 38, 38, 59, 59, 59, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102]


start_trainers = [81, 91, 92, 92, 94, 95]


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

    # If the user is not logged in or their name is not stored in the session, redirect to the login page
    if not player_name:
        return redirect(url_for('login'))

    return render_template('options.html')



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



if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)