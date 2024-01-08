import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Get Player Names and Set Unique Players
def set_players():
    players = []
    player1 = request.form.get("player1")
    player2 = request.form.get("player2")
    player3 = request.form.get("player3")
    player4 = request.form.get("player4")
    player5 = request.form.get("player5")
    player6 = request.form.get("player6")
    if player1: players.append(player1)
    if player2: players.append(player2)
    if player3: players.append(player3)
    if player4: players.append(player4)
    if player5: players.append(player5)
    if player6: players.append(player6)
    unique_players = set(players)
    return players, unique_players


# Add Create Score_IDs based on Player Names and Game Number and Add Players, Game Number, & Score_IDs into hand_total table and scores table
def add_players(players):
    game_number = db.execute("SELECT game_number FROM game_number")[0]['game_number']
    string_game_number = str(game_number)
    score_ids = []
    for player in players:
        score_id = string_game_number+"_"+player
        score_ids.append(score_id)
        hand_total = 0
        db.execute("INSERT INTO scores (score_id, game_number, user_name, hand_total) VALUES (?, ?, ?, ?)", score_id, game_number, player, hand_total)
        db.execute("INSERT INTO hand_total (score_id, game_number, user_name, hand_total) VALUES (?, ?, ?, ?)", score_id, game_number, player, hand_total)
    return score_ids
