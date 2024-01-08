from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Violets

def four_d_painter(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has all unique colors in hand +31
    card_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    unique_colors = db.execute("SELECT COUNT(DISTINCT color) AS count FROM hand WHERE score_id = ?", score_id)[0]['count']
    if card_count == unique_colors:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def holo_host(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the greatest or is tied for the greatest influence count + 18
    game_number = session['game_number']
    card_holder_influence_count = db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count']
    influence_counts = db.execute("SELECT influence_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in influence_counts:
        other_influence_count = row['influence_count']
        if card_holder_influence_count < other_influence_count:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def mickey_the_carver(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If there is at least 1 banished Red +10
    banished_reds = db.execute("SELECT banished_reds AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    if banished_reds >= 1:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has at least 1 Gold in hand +10
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def musician(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has cards with only even cores +32
    odd_core_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE core % ? = ? AND score_id = ?", 2, 1, score_id)[0]['count']
    if odd_core_count == 0:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def reporter(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the greatest or is tied for the greatest helium_count + 29
    game_number = session['game_number']
    card_holder_helium_count = db.execute ("SELECT helium_count FROM scores WHERE score_id = ?", score_id)[0]['helium_count']
    helium_counts = db.execute("SELECT helium_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in helium_counts:
        other_helium_count = row['helium_count']
        if card_holder_helium_count < other_helium_count:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def vlogger(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the greatest or is tied for the greatest fleet_count + 23
    game_number = session['game_number']
    card_holder_fleet_count = db.execute ("SELECT fleet_count FROM scores WHERE score_id = ?", score_id)[0]['fleet_count']
    fleet_counts = db.execute("SELECT fleet_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in fleet_counts:
        other_fleet_count = row['fleet_count']
        if card_holder_fleet_count < other_fleet_count:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def zanzibar(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has cards with only odd cores +31
    even_core_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE core % ? = ? AND score_id = ?", 2, 0, score_id)[0]['count']
    if even_core_count == 0:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
