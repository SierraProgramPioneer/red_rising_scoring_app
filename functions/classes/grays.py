from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Grays

def bridge(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # For each Pink & Violet on all Locations * 5
    pink_count = db.execute("SELECT location_pink AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    violet_count = db.execute("SELECT location_violet AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    pink_violet_count = pink_count + violet_count
    c1p = 5 * pink_violet_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Bridge_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")


def colonel_valentin(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']


    # For each Gold on all Locations * 5
    gold_count = db.execute("SELECT location_gold AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    c1p = 5 * gold_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Colonel Valentin_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")


def danto(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # For each Copper & White on all Locations * 5
    copper_count = db.execute("SELECT location_copper AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    white_count = db.execute("SELECT location_white AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    copper_white_count = copper_count + white_count
    c1p = 5 * copper_white_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Danto_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")


def holiday(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # For each Orange & Blue on all Locations * 5
    orange_count = db.execute("SELECT location_orange AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    blue_count = db.execute("SELECT location_blue AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    orange_blue_count = orange_count + blue_count
    c1p = 5 * orange_blue_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Holiday_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")


def sun_hwa(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # For each Obsidian & Green on all Locations * 5
    obsidian_count = db.execute("SELECT location_obsidian AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    green_count = db.execute("SELECT location_green AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    obsidian_green_count = obsidian_count + green_count
    c1p = 5 * obsidian_green_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Sun-Hwa_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")


def trigg(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # For each Gray & Yellow on all Locations * 5
    gray_count = db.execute("SELECT location_gray AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    yellow_count = db.execute("SELECT location_yellow AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    gray_yellow_count = gray_count + yellow_count
    c1p = 5 * gray_yellow_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Trigg_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")


def ugly_dan(condition):
    results = db.execute ("SELECT score_id, user_name FROM hand WHERE character = ?", condition)
    if results:
        score_id = results[0]['score_id']
        user_name = results[0]['user_name']

    # For each Red & Brown on all Locations * 5
    red_count = db.execute("SELECT location_red AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    brown_count = db.execute("SELECT location_brown AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])[0]['count']
    red_brown_count = red_count + brown_count
    c1p = 5 * red_brown_count
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)

    # Add Additional Color to Hand
    other_color = session['game_end_actions_data']['Ugly Dan_other_color']
    ghost_character = "Ghost" + "_" + condition + "_" + other_color
    check_hand = db.execute("SELECT character FROM hand WHERE character = ?", ghost_character)
    # If not already in hand, add to hand
    if len(check_hand) == 0:
        # Check if Ghost Character already in Character Cards
        result = db.execute("SELECT character FROM character_cards WHERE character = ?", ghost_character)
        # If Not already in Character Cards add to Character Cards
        if len(result) == 0:
            db.execute("INSERT INTO character_cards(character, color, core, c1c, c1p, c2c, c2p) VALUES(?, ?, ?, ?, ?, ?, ?)", ghost_character, other_color, 0, 'N/A', 0, 'N/A', 0)
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
        else:
            db.execute("INSERT INTO hand(score_id, game_number, user_name, character, color, core, c1p, c2p, card_total) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", score_id, session['game_number'], user_name, ghost_character, other_color, 0, 0, 0, 0)
    else:
         print(ghost_character + "" + "Already in Hand")
