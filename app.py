import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session

from helpers import apology, login_required
from functions.players import set_players, add_players
from functions.game_number import update_game_number
from functions.score_house_items import total_house_items
from functions.location_banished import location_banished_process
from functions.score_cards import update_hand, count_cards, score_hand, calculate_conditional_points, total_card_points, total_player_hand
from functions.total_score import sum_points, calculate_winner


# Configure application
app = Flask(__name__)
app.secret_key = 'boba'

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/red_rising.db")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    """Display Home Page"""
    return render_template("index.html")

@app.route("/credits", methods=["GET"])
def credits():
    """Display Credits Page"""
    return render_template("credits.html")


# Establish New Game Scoring
@app.route("/new_game", methods=["GET", "POST"])
def new_game():
    # Clear Past Scoring Tables
    db.execute("DELETE FROM hand")
    db.execute("DELETE FROM hand_total")
    db.execute("DELETE FROM location_banished_results")

    if request.method == "POST":
        # Select Player Numbers
        input = request.form.get("number_players")
        if input is not None:
            number_players = int(input)
            return render_template("new_game.html", number_players = number_players)
        else:
            # Input Names
            number_players = 0
            # Confirm Entered Players are Unique
            players, unique_players = set_players()
            if len(players) != len(unique_players):
                return render_template("apology.html", code = "All Player Names Must be Different")
            else:
                # Add Players into game
                score_ids = add_players(players)

                # Set Session Players, Score_IDs, and Game Number
                session['players']  = players
                session['score_ids'] = score_ids
                session['game_number'] = db.execute("SELECT * FROM game_number")[0]['game_number']

                # Update Game Number for Next Game
                update_game_number()

                # Set Session Characters & Colors that Are Not Ghost Cards
                pattern = 'Ghost%'
                session['colors'] = db.execute("SELECT DISTINCT color FROM character_cards WHERE color NOT LIKE ? ORDER BY color ASC", pattern)
                session['cards'] = db.execute("SELECT color, character FROM character_cards WHERE character NOT LIKE ? ORDER BY color ASC, character ASC", pattern)
                return redirect("/score_house_items")

    # Prompt for New Game Details
    else:
        return render_template("new_game.html")



@app.route("/score_house_items", methods=["GET", "POST"])
def score_house_items():

    # Score House Items
    if request.method == "POST":
        update_value = request.form.get('update')

        # If Submit Value is Update, Update Inputs in Table for Review before Submitting
        if update_value == "update":
            total_house_items(request.form)
            current_house_scores = db.execute("SELECT * FROM scores WHERE game_number = ?", session['game_number'])
            return render_template("score_house_items.html", current_house_scores = current_house_scores)

        # Confirm & Submit House Item Scores
        else:
            return redirect("/location_banished_record")

    # Prompt for House Item Counts
    else:
        return render_template("score_house_items.html")


# Get Banished Card Counts and Counts of Colors on Locations
@app.route("/location_banished_record", methods=["GET", "POST"])
def location_banished_record():

    # Record Banished Cards and Colors on Locations
    if request.method == "POST":
        form_data = dict(request.form)
        location_banished_process(form_data)
        return redirect("/add_cards")

    # Prompt for Banished Card Counts and Counts of Colors on Locations
    else:
        return render_template("location_banished_results.html")


# Add or Remove Cards to Player's Hand
@app.route("/add_cards", methods=["GET", "POST"])
def add_cards():

    # Add or Remove Cards in Hand
    if request.method == "POST":
        # Get Clicked Card Information and Update Hand and Refresh Page with Sesson Cards in Hand
        if request.is_json:
            card = request.get_json()
            update_hand(card)
            session['hand_cards'] = db.execute("SELECT * FROM hand WHERE game_number = ?", session['game_number'])
            return jsonify({'refresh': True})

        # Submit Cards in Hand & Set Session "Game Action Cards"
        else:
            session['hacker'] = db.execute("SELECT character FROM hand WHERE character = ?", "Hacker")
            session['developer'] = db.execute("SELECT character FROM hand WHERE character = ?", "Developer")
            session['grays'] = db.execute("SELECT character FROM hand WHERE color = ?", "Gray")
            session['oranges'] = db.execute("SELECT character FROM hand WHERE color = ?", "Orange")
            return redirect("/game_end_actions")

    # View Cards in Player's Hands
    else:
        session['hand_cards'] = db.execute("SELECT * FROM hand WHERE game_number = ?", session['game_number'])
        return render_template("add_cards.html")


# Gain Game End Action Ghost Cards and Finalize Score
@app.route("/game_end_actions", methods=["GET", "POST"])
def game_end_actions():

    # Calculate Cards with Game End Action Values
    if request.method == "POST":
        game_end_actions_data = dict(request.form)
        session['game_end_actions_data'] = game_end_actions_data

        # Get All Cards from Hand
        hand = db.execute("SELECT * FROM hand")

        # Set Card Count Penalty
        count_cards()

        # Calculate Original Hand's Conditional Point Values
        calculate_conditional_points(hand)

        # Recalculate Hand after Ghost Cards have been Added
        updated_hand = db.execute("SELECT * FROM hand")
        calculate_conditional_points(updated_hand)

        # Score Hand Totals
        score_hand(updated_hand)
        return redirect("/hand_total")

    # Prompt for Game End Action Inputs for Relevant Cards
    else:
        return render_template("game_end_actions.html")


# Sum Hand Total
@app.route("/hand_total", methods=["GET", "POST"])
def hand_total():

    # Add Hand Total, Card Count Penalty, & House Item Points & Calculate Winner
    if request.method == "POST":
        # Post Hand Total to Scores
        sum_points()
        session['winner'] = calculate_winner()
        return render_template("results.html")

    # Review Hand Total
    else:
        session['hand_cards'] = db.execute("SELECT * FROM hand WHERE game_number = ?", session['game_number'])
        return render_template("hand_total.html")

# Game Score History
@app.route("/history")
def history():
    # Show All Past Game Records
    past_games = db.execute("SELECT * FROM scores")
    return render_template("history.html", past_games = past_games)


# View Character Cards
@app.route("/character_cards")
def character_cards():
    # Show All Cards in Game
    pattern = 'Ghost%'
    character_cards = db.execute("SELECT color, character FROM character_cards WHERE character NOT LIKE ? ORDER BY color ASC, character ASC", pattern)
    return render_template("character_cards.html", character_cards = character_cards)


