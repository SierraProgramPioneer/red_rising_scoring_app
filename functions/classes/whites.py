from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Whites

def judge(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each card in card holder hand * 3
    card_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    c1p = 3 * card_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def justice(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']
    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def magistrate(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has 3 or more Fleet count, Influence Count, and Helium Count +15
    card_holder_fleet_count = db.execute ("SELECT fleet_count FROM scores WHERE score_id = ?", score_id)[0]['fleet_count']
    card_holder_influence_count = db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count']
    card_holder_helium_count = db.execute ("SELECT helium_count FROM scores WHERE score_id = ?", score_id)[0]['helium_count']
    if card_holder_fleet_count >= 3 and card_holder_influence_count >= 3 and card_holder_helium_count >= 3:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def martyr(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def orator(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder does not have the Sovereign token +21
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "no":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def priestess(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has cards with core values of 20 or or more + 20
    cards_under_twenty = db.execute("SELECT COUNT (*) AS count FROM hand WHERE core < ? AND score_id = ?", 20, score_id)[0]['count']

    if cards_under_twenty == 0:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def seer(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Sovereign token +11
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

