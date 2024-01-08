from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Browns

def artisan_chef(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Gold in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Gold", score_id)
    golds_in_player_hand = int(result[0]['count'])
    c1p = 5 * golds_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def assassin(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Obsidian in player's hand * 10
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color = ? AND score_id =?", "Obsidian", score_id)
    obsidians_in_player_hand = int(result[0]['count'])
    c1p = 10 * obsidians_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def gardener(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Violet & Pink in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color IN (?, ?) AND score_id =?", "Violet", "Pink", score_id)
    violet_pink_in_player_hand = int(result[0]['count'])
    c1p = 5 * violet_pink_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def janitor(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Green, Yellow, and Blue in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color IN (?, ?, ?) AND score_id =?", "Green", "Yellow", "Blue", score_id)
    green_yellow_blue_in_player_hand = int(result[0]['count'])
    c1p = 5 * green_yellow_blue_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def mess_hall_cook(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Gray & Orange in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color IN (?, ?) AND score_id =?", "Gray", "Orange", score_id)
    gray_orange_in_player_hand = int(result[0]['count'])
    c1p = 5 * gray_orange_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def modjob(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Red & Brown in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color IN (?, ?) AND score_id =?", "Red", "Brown", score_id)
    red_brown_in_player_hand = int(result[0]['count'])
    c1p = 5 * red_brown_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


def nanny(condition):
    score_id = db.execute ("SELECT score_id FROM hand WHERE character = ?", condition)[0]['score_id']

    # For each Silver, White, and Copper in player's hand * 5
    result = db.execute("SELECT COUNT(*) AS count FROM hand WHERE color IN (?, ?, ?) AND score_id =?", "Silver", "White", "Copper", score_id)
    silver_white_copper_in_player_hand = int(result[0]['count'])
    c1p = 5 * silver_white_copper_in_player_hand
    db.execute("UPDATE hand SET c1p = ?, c2p = ? WHERE character = ? AND score_id = ?", c1p, 0, condition, score_id)


