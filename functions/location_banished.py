import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session


db = SQL("sqlite:///database/red_rising.db")

# Get Location and Banished Cards Information and Add Into location_banished_results table to be used in Final Hand Scoring
def location_banished_process(form_data):
    db.execute("INSERT INTO location_banished_results (game_number) VALUES (?)", session['game_number'])
    for key, value in form_data.items():
        if value is None or value == "":
            value = 0
        query = f"UPDATE location_banished_results SET {key} = ? WHERE game_number = ?"
        db.execute(query, value, session['game_number'])




