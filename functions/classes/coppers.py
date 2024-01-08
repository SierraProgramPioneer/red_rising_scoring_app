from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Coppers

def administrator(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the least or is tied for the least influence count + 15
    game_number = session['game_number']
    card_holder_influence_count = db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count']
    influence_counts = db.execute("SELECT influence_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in influence_counts:
        other_influence_count = row['influence_count']
        if card_holder_influence_count > other_influence_count:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def auctioneer(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def bondilus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Sovereign token +5
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has at least 1 Gold in hand +5
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def diplomat(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder and any opponent have the exact same amount of Influence on the Institute +19
    game_number = session['game_number']
    card_holder_influence_count = db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count']
    influence_counts = db.execute("SELECT influence_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in influence_counts:
        other_influence_count = row['influence_count']
        if card_holder_influence_count == other_influence_count:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def lawyer(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Judge +22
    judge_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Judge%", score_id)
    if judge_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has a White  in hand (not the Judge) + 12
    white_result = db.execute("SELECT 1 FROM hand WHERE (character NOT LIKE ?) AND color = ? AND score_id = ?", "Judge%", "White", score_id)
    if white_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def politician(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the most Influence on the Institute (or tied for the most)	15
    game_number = session['game_number']
    card_holder_influence_count = db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count']
    influence_counts = db.execute("SELECT influence_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in influence_counts:
        other_influence_count = row['influence_count']
        if card_holder_influence_count < other_influence_count:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def timony(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Multiply card holder's influence count by 3
    card_holder_influence_count = int(db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count'])
    c1p = 3 * card_holder_influence_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)
