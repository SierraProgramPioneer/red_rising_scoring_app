from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Obsidians

def alfrun(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Nero in hand +10
    nero_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Nero%", score_id)
    if nero_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Jopho in hand	+10
    jopho_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Jopho%", score_id)
    if jopho_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def alia_snow_sparrow(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has only Gold, Grays, and/ or Obsidian cards +24
    other_color_count = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color NOT IN (?, ?, ?) AND score_id = ?", "Gold", "Gray", "Obsidian", score_id)[0]['count']
    if other_color_count == 0:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def helga(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Pax au Telemanus or The Pax in hand +14
    result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Pax Au Telemanus%", "%The Pax%", score_id)
    if result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def jopho(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Nero in hand +10
    nero_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Nero%", score_id)
    if nero_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Alfrun in hand	+10
    alfrun_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Alfrun%", score_id)
    if alfrun_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def ragnar(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has an Orange in hand	+10
    orange_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Orange", score_id)
    if orange_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Sefi +10
    sefi_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Sefi%", score_id)
    if sefi_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def sefi(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Ragnar	in hand +20
    ragnar_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Ragnar%", score_id)
    if ragnar_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # For each Gold	in card holder hand -5

    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    golds_in_player_hand = int(result[0]['count'])
    print(golds_in_player_hand)
    c2p = -5 * golds_in_player_hand
    print(c2p)
    db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", c2p, condition, score_id)


def stained(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder's only Obsidian is Stained +15
    obsidian_result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Obsidian", score_id)
    if int(obsidian_result[0]['count']) == 1:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
