from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Silvers

def banker(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']
    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def ceo(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has at least 5 helium_count +18
    card_holder_helium_count = int(db.execute ("SELECT helium_count FROM scores WHERE score_id = ?", score_id)[0]['helium_count'])
    if card_holder_helium_count >= 5:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def investor(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']
    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def loan_shark(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has 7 or more cards +7
    card_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    if card_count >= 7:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def quicksilver(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder's helium is less than any other player -30
    game_number = session['game_number']
    card_holder_helium_count = db.execute ("SELECT helium_count FROM scores WHERE score_id = ?", score_id)[0]['helium_count']
    helium_counts = db.execute("SELECT helium_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in helium_counts:
        other_helium_count = row['helium_count']
        if card_holder_helium_count < other_helium_count:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def sponsor(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Multiply card holder's influence count by 2
    card_holder_influence_count = int(db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count'])
    c1p = 2 * card_holder_influence_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def stock_broker(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Helium in card holders helium_count * 5 (Max 25 Points)
    card_holder_helium_count = int(db.execute ("SELECT helium_count FROM scores WHERE score_id = ?", score_id)[0]['helium_count'])
    if card_holder_helium_count > 5:
        card_holder_helium_count = 5
    c1p = 5 * card_holder_helium_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)
