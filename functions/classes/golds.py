from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Golds

def aja(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Octavia + 15
    result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Octavia%", score_id)
    if result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def antonia(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has The Jackal or 2 other Golds + 15
    jackal_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%The Jackal%", score_id)
    if jackal_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        gold_result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Gold", score_id)
        if int(gold_result[0]['count']) >= 2:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Victra or Sevro -10 (Artisan Chef clears Gold penalties)
    artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
    if artisan_chef_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        victra_sevro_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Victra%", "%Sevro%", score_id)
        victra_sevro_result = db.execute("SELECT 1 FROM hand WHERE character in (?, ?) AND score_id = ?", "Victra", "Sevro", score_id)
        if victra_sevro_result:
            db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
        else:
            db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def ash_lord(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Blue in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Blue", score_id)
    blue_in_player_hand = int(result[0]['count'])
    c1p = 5 * blue_in_player_hand
    db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", c1p, condition, score_id)

    # For each Banished Blue * 5
    result2 = db.execute("SELECT banished_blues AS count FROM location_banished_results WHERE game_number = ?", session['game_number'])
    banished_blues = int(result2[0]['count'])
    c2p = 5 * banished_blues
    db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", c2p, condition, score_id)


def bone_riders(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Jackal or a Gray +15

    jackal_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%The Jackal%", score_id)
    if jackal_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        return
    else:
        result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Gray", score_id)
        if result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def cassius(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has both Mustang & Darrow	+40
    mustang_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Mustang%", score_id)
    if mustang_result:
        darrow_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Darrow%", score_id)
        if darrow_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
            return
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            return

    # If card holder has Darrow (but not Mustang) -20 (Artisan Chef clears Gold penalties)
    else:
        artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
        if artisan_chef_result:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
        else:
            darrow_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Darrow%", score_id)
            if darrow_result:
                db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?), c1p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
            else:
                db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def fitchner(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has at least 1 Red +10
    red_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Red", score_id)
    if red_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Sevro + 10
    sevro_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Sevro%", score_id)
    if sevro_result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def karnus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Cassius +30
    cassius_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Cassius%", score_id)
    if cassius_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card hodler has Mustang, The Jackal, or Nero -15 (Artisan Chef clears Gold penalties)
    artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
    if artisan_chef_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        mustang_jackal_nero_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ? OR character LIKE ?) AND score_id = ?", "%Mustang%", "%The Jackal%", "%Nero%", score_id)
        if mustang_jackal_nero_result:
            db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
        else:
            db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def lorn(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has no other Golds in hand +15
    gold_result = db.execute("SELECT 1 FROM hand WHERE character != ? AND color = ? AND score_id = ?", condition, "Gold", score_id)
    if gold_result:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def lysander(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Sovereign Token + 20
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        return

    # If card holder has Octavia or Cassius	+20
    else:
        result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Octavia%", "%Cassius%", score_id)
        if result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def mustang(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each unique color in card holder's hand * 5
    unique_colors = db.execute("SELECT COUNT(DISTINCT color) AS count FROM hand WHERE score_id = ? AND color != ?", score_id, "Ghost")[0]['count']
    c1p = 5 * unique_colors
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def nero(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Sovereign Token +10
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Cassius, Karnus, and Octavia -5 for each (Artisian Chef Clears Gold Penalties)
    artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
    if artisan_chef_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ? OR character LIKE ?) AND score_id = ?", "%Cassius%", "%Karnus%", "%Octavia%", score_id)
        if result:
            cassius_karnus_octavia_in_player_hand = int(result[0]['count'])
            c2p = -5 * cassius_karnus_octavia_in_player_hand
            db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", c2p, condition, score_id)
        else:
            db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)



def octavia(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder doesn't have either the Sovereign Token or Lysander -30 (Artisian Chef Clears Gold Penalties)
    artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
    if artisan_chef_result:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
    else:
        sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
        if sovereign_result[0]['sovereign_token'] == "yes":
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
        else:
            lysander_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Lysander%", score_id)
            if lysander_result:
                db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)
            else:
                db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)


def pax_au_telemanus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Mustang +20
    mustang_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Mustang%", score_id)
    if mustang_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        return
    else:
        # If card holder has an Obsidian +20
        obsidian_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Obsidian", score_id)
        if obsidian_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def romulus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Sovereign Token +15
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Roque or Octavia or without a Blue -25 (Artisian Chef Clears Gold Penalties)
    artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
    if artisan_chef_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        roque_octavia_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Roque%", "%Octavia%", score_id)
        if roque_octavia_result:
            db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
        else:
            blue_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Blue", score_id)
            if blue_result:
                db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
            else:
                db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)


def roque(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Blue in card holder's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Blue", score_id)
    blues_in_player_hand = int(result[0]['count'])
    c1p = 5 * blues_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def sevro(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Victra or The Howlers in hand +20
    victra_howlers_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Victra%", "%The Howlers%", score_id)
    if victra_howlers_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        return

    # If card holder has a Red in hand	+20
    else:
        red_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Red", score_id)
        if red_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def tactus(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Octavia or Darrow in hand +20
    octavia_darrow_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Octavia%", "%Darrow%", score_id)
    if octavia_darrow_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        return

    # If card holder has a Pink in hand +20
    else:
        pink_result = db.execute("SELECT 1 FROM hand WHERE color = ? AND score_id = ?", "Pink", score_id)
        if pink_result:
            db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
        else:
            db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def the_howlers(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Sevro +15
    sevro_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Sevro%", score_id)
    if sevro_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def the_jackal(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has the Sovereign Token +30
    sovereign_result = db.execute("SELECT sovereign_token FROM scores WHERE score_id = ?", score_id)
    if sovereign_result[0]['sovereign_token'] == "yes":
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Darrow or Octavia in hand -30 (Artisian Chef Clears Gold Penalties)
    artisan_chef_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%Artisan Chef%", score_id)
    if artisan_chef_result:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
    else:
        octavia_darrow_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Octavia%", "%Darrow%", score_id)
        if octavia_darrow_result:
            db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
        else:
            db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)


def the_telemanuses(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has Pax au Telemanus and/or The Pax +15
    result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ? OR character LIKE ?) AND score_id = ?", "%Pax Au Telemanus%", "%The Pax%", score_id)
    if result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?), c2p = ? WHERE character = ? AND score_id = ?", condition, 0, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", 0, 0, condition, score_id)


def victra(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # If card holder has The Howlers in hand +10
    howlers_result = db.execute("SELECT 1 FROM hand WHERE (character LIKE ?) AND score_id = ?", "%The Howlers%", score_id)
    if howlers_result:
        db.execute("UPDATE hand SET c1p = (SELECT c1p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c1p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)

    # If card holder has Sevro or Darrow in hand +10
    result = db.execute("SELECT 1 FROM hand WHERE character IN (?, ?) AND score_id = ?", "Sevro", "Darrow", score_id)
    if result:
        db.execute("UPDATE hand SET c2p = (SELECT c2p FROM character_cards WHERE character = ?) WHERE character = ? AND score_id = ?", condition, condition, score_id)
    else:
        db.execute("UPDATE hand SET c2p = ? WHERE character = ? AND score_id = ?", 0, condition, score_id)
