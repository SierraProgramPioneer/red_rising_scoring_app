from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Pinks

def calliope(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has The Jackal +20
    jackal_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%The Jackal%", score_id)
    if jackal_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def conversationalist(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has a White in hand +15
    white_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "White", score_id)
    if white_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def evey(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Darrow in hand	+15
    darrow_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Darrow%", score_id)
    if darrow_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Mickey the Carver in hand	-15
    mickey_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Mickey the Carver%", score_id)
    if mickey_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def garden_trained_rose(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has at least one Silver in hand +14
    silver_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Silver", score_id)
    if silver_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def masseuse(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has a Copper in hand +16
    copper_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Copper", score_id)
    if copper_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def matteo(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Quicksilver + 17
    quicksilver_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Quicksilver%", score_id)
    if quicksilver_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        return

    # If card holder has another pink +17
    else:
        pink_result = db.execute("SELECT 1 FROM hand WHERE character != ? AND color = ? AND score_id = ?", condition, "Pink", score_id)
        if pink_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def theodora(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has a Gold or Red in hand but not both	+14

    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        red_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Red", score_id)
        if red_result:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        red_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Red", score_id)
        if red_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
