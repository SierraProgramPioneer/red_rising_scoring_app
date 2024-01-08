import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from functions.conditions import *
from datetime import datetime

db = SQL("sqlite:///database/red_rising.db")

#   Sum House Item Scores, Hand Total, and Card Penalty for each Player in Game
def sum_points():
    score_ids = session['score_ids']
    for score_id in score_ids:
        current_house_score = db.execute("SELECT hand_total FROM scores WHERE score_id = ?", score_id)[0]['hand_total']
        print(current_house_score)
        hand_total = db.execute("SELECT hand_total FROM hand_total WHERE score_id = ?", score_id)[0]['hand_total']
        print(hand_total)
        card_penalty = db.execute("SELECT card_count_score FROM scores WHERE score_id = ?", score_id)[0]['card_count_score']
        print(card_penalty)
        final_score = current_house_score + hand_total + card_penalty
        print(card_penalty)
        db.execute("UPDATE scores SET hand_total = ? WHERE score_id = ?", final_score, score_id)


#   Compare Total Points of each Player and Determine the Game's Winner
def calculate_winner():
    winner = db.execute("SELECT user_name FROM scores WHERE hand_total = (SELECT MAX(hand_total) FROM scores WHERE game_number = ?) AND game_number = ?", session['game_number'], session['game_number'])[0]['user_name']
    date = datetime.now()
    for player in session['players']:
        if player == winner:
            db.execute("UPDATE scores SET result = ?, date = ? WHERE game_number = ? AND user_name = ?", "Won", date.strftime("%m/%d/%Y"), session['game_number'], player)
        else:
            db.execute("UPDATE scores SET result = ?, date = ? WHERE game_number = ? AND user_name = ?", "Lost", date.strftime("%m/%d/%Y"), session['game_number'], player)

    return winner
