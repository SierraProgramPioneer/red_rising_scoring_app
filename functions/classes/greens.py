from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Greens

def codebreaker(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If each card in a player's hand starts with a different character +22
    card_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    unique_letters = db.execute("SELECT COUNT(DISTINCT SUBSTR(character, 1,1)) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    if card_count == unique_letters:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def dataport_specialist(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has at least 1 Blue in hand +26
    blue_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Blue", score_id)
    if blue_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)



def developer(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']
    top_core =  session['game_end_actions_data']['top_core_hacker']

    # Gain the points equivelant to the Core of the top card of any location +?
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", top_core, 0, condition, score_id)


def firewall_expert(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If there is at least 1 location with no cards or where the top card is face down +22
    result = db.execute("SELECT none_face_down AS result FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['result']
    if result == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def hacker(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']
    top_core =  session['game_end_actions_data']['top_core_hacker']

    # Update c1p to reflect Core value of Top Card From Deck
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", top_core, 0, condition, score_id)


def holo_designer(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has at least 1 Violet in hand +28
    violet_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Violet", score_id)
    if violet_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def online_gambler(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']
    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)



