import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from functions.house_details import item_counts, calculate_fleet, calculate_helium, calculate_sovereign, calculate_influence


db = SQL("sqlite:///database/red_rising.db")

#   Total Points for Each Player's House Items
def total_house_items(form_data):

    # Check Which Player has Soveriegn Token
    sovereign_token_holder = form_data.get('sovereign_token_holder')

    # Set House Item Counts and Scores
    for player in session['players']:
        # Set House Item Counts
        fleet_count, helium_count, influence_count, _ = item_counts(player, form_data)

        # Calculate Fleet Score
        if fleet_count == '':
            fleet_count = 0
        fleet_score = calculate_fleet(int(fleet_count))

        # Calculate Helium Score
        if helium_count == '':
            helium_count = 0
        helium_score = calculate_helium(int(helium_count))

        # Update Influence Count    (Influence Score Must be calculate after all Player's Influence Counts are Entered)
        if influence_count == '':
            influence_count = 0

        # Update Sovereign Token Score
        sovereign_token, sovereign_score = calculate_sovereign(player, sovereign_token_holder)

        # Add Counts and Scores to Scores Table
        for score_id in session['score_ids']:
            db.execute("UPDATE scores SET fleet_count = ?, fleet_score = ? WHERE score_id = ? AND user_name = ?", fleet_count, fleet_score, score_id, player)
            db.execute("UPDATE scores SET helium_count = ?, helium_score = ? WHERE score_id = ? AND user_name = ?", helium_count, helium_score, score_id, player)
            db.execute("UPDATE scores SET influence_count = ? WHERE score_id = ? AND user_name = ?", influence_count, score_id, player)
            db.execute("UPDATE scores SET sovereign_token = ?, sovereign_score = ? WHERE score_id = ? AND user_name = ?", sovereign_token, sovereign_score, score_id, player)


    # Calculate Influence Scores Based on Other Player's Influence Counts
    for player in session['players']:
        influence_count = form_data.get(f"{player}_influence_count")
        if influence_count == '':
            influence_count = 0
        calculate_influence(int(influence_count), player)


    # Total Current Score from House Items
    for score_id in session['score_ids']:
        result = db.execute("SELECT fleet_score, helium_score, influence_scores, sovereign_score FROM scores WHERE score_id = ?", score_id)[0]
        fleet_score = result['fleet_score']
        helium_score = result['helium_score']
        influence_scores = result['influence_scores']
        sovereign_score = result['sovereign_score']
        current_score = fleet_score + helium_score + influence_scores + sovereign_score
        db.execute("UPDATE scores SET hand_total = ? WHERE score_id = ?", current_score, score_id)
