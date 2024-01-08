from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Oranges

def aegis_craftsman(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has a Gold	+10
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has no Obsidians +10
    obsidian_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Obsidian", score_id)
    if obsidian_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Aegis Craftsman_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "" + "Already in Hand")





def artificer(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has both another Orange and a Gold	+20
    orange_result = db.execute("SELECT 1 FROM hand WHERE character != ? AND color = ? AND score_id = ?", condition, "Orange", score_id)
    if orange_result:
        gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
        if gold_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Artificer_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "Already in Hand")


def cyther(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has at least 1 Blue in hand +16
    blue_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Blue", score_id)
    if blue_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Cyther_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "Already in Hand")


def gravboot_cobbler(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has a Gold or Gray in hand	+14
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        gray_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gray", score_id)
        if gray_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Gravboot Cobbler_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "Already in Hand")


def pulse_armorer(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has at least 1 Gray in hand +17
    gray_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gray", score_id)
    if gray_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Pulse Armorer_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "Already in Hand")


def pulse_fist_engineer(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has at least 1 Obsidian in hand +18
    obsidian_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Obsidian", score_id)
    if obsidian_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Pulse Fist Engineer_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "Already in Hand")


def razor_designer(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # If card holder has at least 1 Gold and NO Obsidians in hand +13
    gold_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gold", score_id)
    if gold_result:
        obsidian_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Obsidian", score_id)
        if obsidian_result:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)

    # Add Character Name to Hand
    other_character = session['game_end_actions_data']['Razor Designer_change_character']
    ghost_character = "Ghost" + "_" + other_character + "_" + user_name
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, 'Ghost', 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, 'Ghost', 0, 0, 0, 0)

    else:
        print(ghost_character + "Already in Hand")
