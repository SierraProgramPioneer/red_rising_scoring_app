import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

db = SQL("sqlite:///database/red_rising.db")

#   Update the Game Number to Prepare for the Next Game
def update_game_number():
    """Update Game Number"""
    game_number = db.execute("SELECT game_number FROM game_number")[0]['game_number']
    game_number_new = game_number + 1
    db.execute("UPDATE game_number SET game_number = ?", game_number_new)
    return
