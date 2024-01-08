from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Reds

def arlus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has no Golds in hand +25
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def dancer(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has no Grays in hand +11
    gray_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gray", score_id)
    if gray_result:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)

    # If card holder has no Golds in hand +11
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gray_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)


def darrow(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has 7 or more cards +30
    card_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    if card_count >= 7:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def deanna(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has another Red in hand +26
    red_result = db.execute("SELECT 1 FROM hand WHERE character != ? AND color = ? AND score_id = ?", condition, "Red", score_id)
    if red_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def eo(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each other Red in card holder hand * 10
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE character != ? AND color = ? AND score_id =?", condition, "Red", score_id)
    red_in_player_hand = int(result[0]['count'])
    c1p = 10 * red_in_player_hand
    db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", c1p, condition, score_id)

    # If card holder has a Gray  in hand -10 unless Gray card is Bridge
    gray_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gray", score_id)
    if gray_result:
        result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Gray", score_id)
        grays_in_player_hand = int(result[0]['count'])
        if grays_in_player_hand > 1:
            db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
        else:
            gray_character = db.execute("SELECT character FROM hand WHERE color = ? AND score_id = ?", "Gray", score_id)[0]['character']
            if gray_character == "Bridge" or gray_character == "Ghost_Bridge":
                db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
            else:
                db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def harmony(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has only Red, Pink, Brown, or Obsidian cards +33
    other_color_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color NOT IN (?, ?, ?, ?) AND score_id = ?", "Red", "Pink", "Brown", "Obsidian", score_id)[0]['count']
    if other_color_count == 0:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def uncle_narol(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has cards with core values of 10 or less + 40
    cards_over_ten = db.execute("SELECT COUNT (*) AS count FROM hand WHERE core > ? AND score_id = ?", 10, score_id)[0]['count']

    if cards_over_ten == 0:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

