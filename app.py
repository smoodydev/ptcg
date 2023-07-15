import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session, send_file, url_for
from flask_pymongo import PyMongo, ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

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

    return render_template('profile.html', player_name=player_name)

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









@app.route('/select_option', methods=["GET", "POST"])
def select_option():
    if request.method == "POST":
        if "coin" not in session:
            print(request.form["option"])
    # Access the logged-in user's name from the session
    player_name = session.get('player_name')

    # If the user is not logged in or their name is not stored in the session, redirect to the login page
    if not player_name:
        return redirect(url_for('login'))

    return render_template('options.html')







if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)