import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from functions.conditions import *

db = SQL("sqlite:///database/red_rising.db")

# Add Card to Hand
def update_hand(card):
    game_number = card['game_number']
    user_name = card['user_name']
    score_id = game_number + "_" + user_name
    character = card['character']

    # Check if Card Already in Hand & Delete if Yes
    in_hand = db.execute("SELECT character FROM hand WHERE character = ?", character)
    if len(in_hand) > 0:
        db.execute("DELETE FROM hand WHERE character = ?", character)

    # If Card not in Hand, Add Card to hand table for Appropriate Player
    else:
        character_info = db.execute("SELECT color, core FROM character_cards WHERE character = ?", character)[0]
        color = character_info['color']
        core = character_info['core']

        db.execute("INSERT INTO hand (score_id, game_number, user_name, character, color, core) VALUES (?, ?, ?, ?, ?, ?)", score_id, game_number, user_name, character, color, core)


# Calculate C1 & C2 Points Based on Conditions
def calculate_conditional_points(hand):
    conditions = []
    for row in hand:
        conditions.append(row['character'])
    for condition in conditions:
        if condition in function_map:
            function_map[condition](condition)
        else:
            print("Function not found in map")


# Calculate Penalty for Cards Over 7 (-10 for each Card in Player's Hand Over 7)
def count_cards():
    for score_id in session['score_ids']:
        cards_in_hand = db.execute("SELECT score_id, COUNT(*) as count FROM hand WHERE score_id = ?", score_id)[0]['count']
        if cards_in_hand <= 7:
            db.execute("UPDATE scores SET card_count_score = ? WHERE score_id = ?", 0, score_id)
        else:
            cards_over = cards_in_hand - 7
            penalty = cards_over * -10
            db.execute("UPDATE scores SET card_count_score = ? WHERE score_id = ?", penalty, score_id)


# Score All Cards in Player's Hand
def score_hand(updated_hand):
    total_card_points(updated_hand)
    total_player_hand(updated_hand)


# Total Each Card's Total Points Based on Core + C1P + C2P
def total_card_points(updated_hand):
    for row in updated_hand:
        character = row['character']
        core = db.execute ("SELECT core FROM hand WHERE character = ?", character)[0]['core']
        c1p = db.execute ("SELECT c1p FROM hand WHERE character = ?", character)[0]['c1p']
        if c1p is None:
            c1p = 0
            db.execute ("UPDATE hand SET c1p = ? WHERE character = ?", c1p, character)
        c2p = db.execute ("SELECT c2p FROM hand WHERE character = ?", character)[0]['c2p']
        if c2p is None:
            c2p = 0
            db.execute ("UPDATE hand SET c2p = ? WHERE character = ?", c2p, character)
        card_total = core + c1p + c2p
        db.execute("UPDATE hand SET card_total = ? WHERE character = ?", card_total, row['character'])


# Total Player's Current Score + The Total of Each Card in Hand 
def total_player_hand(updated_hand):
    for row in updated_hand:
        character = row['character']
        score_id = db.execute("SELECT score_id FROM hand WHERE character = ?", character)[0]['score_id']
        current_hand_total = db.execute("SELECT hand_total FROM hand_total WHERE score_id = ?", score_id)[0]['hand_total']
        current_card_total = db.execute("SELECT card_total FROM hand WHERE character = ? AND score_id = ?", character, score_id)[0]['card_total']
        new_hand_total = current_hand_total + current_card_total
        db.execute("UPDATE hand_total SET hand_total = ? WHERE score_id = ?", new_hand_total, score_id)






