from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Blues

def invictus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the greatest or is tied for the greatest fleet_count + 16 else - 9
    game_number = session['game_number']
    card_holder_fleet_count = db.execute ("SELECT fleet_count FROM scores WHERE score_id = ?", score_id)[0]['fleet_count']
    fleet_counts = db.execute("SELECT fleet_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in fleet_counts:
        other_fleet_count = row['fleet_count']
        if card_holder_fleet_count < other_fleet_count:
            db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?), c1p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)



def morning_star(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder does not have Orion, Virga, or Pelus -15
    result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ? OR character LIKE ?) AND score_id = ?", "%Orion%", "%Virga%", "%Pelus%", score_id)
    if result:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def orion(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Pax au Telemanus or The Pax + 10
    result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Pax Au Telemanus%", "%The Pax%", score_id)
    if result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # Gain points equal to your position on the Fleet Track
    card_holder_fleet_count = db.execute ("SELECT fleet_count FROM scores WHERE score_id = ?", score_id)[0]['fleet_count']
    db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", card_holder_fleet_count, condition, score_id)


def pelus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder's fleet track position is 5-7 +20, if fleet track position is 8-10 +35
    card_holder_fleet_count = db.execute ("SELECT fleet_count FROM scores WHERE score_id = ?", score_id)[0]['fleet_count']
    if 5 <= card_holder_fleet_count <= 7:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    elif 8 <= card_holder_fleet_count <= 10:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?), c1p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def quietus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the greatest or is tied for the greatest influence count + 16
    game_number = session['game_number']
    card_holder_influence_count = db.execute ("SELECT influence_count FROM scores WHERE score_id = ?", score_id)[0]['influence_count']
    influence_counts = db.execute("SELECT influence_count FROM scores WHERE game_number = ? AND  score_id != ?", game_number, score_id)
    for row in influence_counts:
        other_influence_count = row['influence_count']
        if card_holder_influence_count < other_influence_count:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return
    db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def the_pax(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Darrow, Sevro, Orion, Virga, or Pelus +15
    result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ? OR character LIKE ? OR character LIKE ? OR character LIKE ?) AND score_id = ?", "%Darrow%", "%Sevro%", "%Orion%", "%Virga%", "%Pelus%", score_id)
    if result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def virga(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder's fleet track position is 6-8 +15, if fleet track position is 9 or 10 +30
    card_holder_fleet_count = db.execute ("SELECT fleet_count FROM scores WHERE score_id = ?", score_id)[0]['fleet_count']
    if 6 <= card_holder_fleet_count <= 8:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    elif 8 < card_holder_fleet_count <= 10:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?), c1p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


