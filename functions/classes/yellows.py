from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Yellows

def dr_virany(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def group_counselor(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Banished Cards -1
    banished_count = db.execute("SELECT banished_count AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    c1p = 1 * banished_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def hypnotist(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def pathologist(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If there are 5-9 Banished Cards +10
    banished_count = db.execute("SELECT banished_count AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    if 5 <= banished_count <= 9:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    # If there are 10+ Banished Cards +25
    elif banished_count >= 10:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?), c1p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)

    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def psychologist(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # Update c1p and c2p to 0
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def researcher(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If there are 4 or fewer Banished Cards + 17
    banished_count = db.execute("SELECT banished_count AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    if banished_count <= 4:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def surgeon(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Gold in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Gold", score_id)
    golds_in_player_hand = int(result[0]['count'])
    c1p = 5 * golds_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)
