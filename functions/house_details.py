import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

# Get the Values of Player's House Items
def item_counts(player, form_data):
    fleet_count = form_data.get(f"{player}_fleet_count")
    helium_count = form_data.get(f"{player}_helium_count")
    influence_count = form_data.get(f"{player}_influence_count")
    sovereign_token = form_data.get(f"{player}_sovereign")
    return fleet_count, helium_count, influence_count, sovereign_token


# Calculate Fleet Score based on Fleet Track Dictionary Point Values
def calculate_fleet(fleet_count):
    fleet_dict = {
        0 : 0,
        1 : 1,
        2 : 3,
        3 : 6,
        4 : 10,
        5 : 15,
        6 : 21,
        7 : 28,
        8 : 34,
        9 : 39,
        10 : 43
    }
    return fleet_dict.get(fleet_count)


# Calculate Helium Score Based on Helium Count * 3
def calculate_helium(helium_count):
    helium_score = int(helium_count) * 3
    return helium_score


# Calculate Points for Sovereign Token (0 if Player does not have Token, +10 if Player has Token)
def calculate_sovereign(player, sovereign_token_holder):
    if player == sovereign_token_holder:
        sovereign_token = "yes"
        sovereign_score = 10
    else:
        sovereign_token = "no"
        sovereign_score = 0
    return sovereign_token, sovereign_score


# Calculate Influence Score Based on Other Players' Influence Counts
def calculate_influence(influence_count, player):
    number_players = len(session['players'])
    score_ids = session['score_ids']

    # Score for 2 Players (Add 3 Influence to Institute Count as a "Ghost Player" -- Greatest Influence Count Scores Influence Count * 4, Second Greatest Influence Count Scores Influence Count * 2, All other Influence Counts Scores Influence Count * 1)
    if number_players == 2:
        values = [3,]
        rows = db.execute("SELECT influence_count FROM scores WHERE game_number = ?", session['game_number'])
        for row in rows:
            values.append(row["influence_count"])
        greatest = max(values)
        values.sort(reverse=True)
        second_greatest = values[1]

        if influence_count == int(greatest):
            influence_score = influence_count * 4
        elif influence_count == int(second_greatest):
            influence_score = influence_count * 2
        else:
            influence_score = influence_count * 1

        db.execute("UPDATE scores SET influence_scores = ? WHERE user_name = ? AND score_id IN (?)", influence_score, player, score_ids)

    # Score for 3 or more Players (Greatest Influence Count Scores Influence Count * 4, Second Greatest Influence Count Scores Influence Count * 2, All other Influence Counts Scores Influence Count * 1)
    else:
        values = []
        rows = db.execute("SELECT influence_count FROM scores WHERE game_number = ?", session['game_number'])
        for row in rows:
            values.append(row["influence_count"])
        greatest = max(values)
        values.sort(reverse=True)
        second_greatest = values[1]

        if influence_count == int(greatest):
            influence_score = influence_count * 4
        elif influence_count == int(second_greatest):
            influence_score = influence_count * 2
        else:
            influence_score = influence_count * 1

        db.execute("UPDATE scores SET influence_scores = ? WHERE user_name = ? AND score_id IN (?)", influence_score, player, score_ids)
