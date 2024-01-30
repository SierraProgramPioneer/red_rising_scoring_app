# Red Rising Scoring App

#### By __**Melissa Parker**__

#### A scoring app for the Red Rising Board Game

#### Video Demo:  https://youtu.be/4aLTRR7fWRg

## Technologies Used

* Python
* Flask
* SQLite3
* JavaScript
* HTML
* CSS
* Jinja2

## Description

The Red Rising Scoring App exists to improve  the enjoyment of playing the Red Rising Board Game by providing a fast and efficient way to calculate game scoring vs. calculating the scores manually.  The app gathers the count of each player's House Items and calculates those points.  Then players are prompted for the cards within their hands.  The application then runs several comparisons to total not only the core points of each card but also the conditional points the card did or did not score.

## Application Set Up & Navigation

##### **Site Navigation:**
* **Home:** Home screen welcomes user and prompts user to score a new game
* **Score a New Game:** Starts a new game to score, detailed in the Implementation of Scoring section
* **Past Scores:**  A table detailing the scores of all past games
* **Credits:**  A page giving credit to Pierce Brown the author of the Red Rising Series and to Stonemaier Games, the creator the Red Rising Board Game


##### **Implementation of Scoring:**
App.py implements the following routes which each accomplish an import aspect of scoring a new game.


* **@app.route(“/new_game”):**
    * Established New Game Scoring by clearing past scoring from the hand, hand_total, and location_banished_results tables.
    * User is prompted for the number of players in the game using a drop-down menu with options 2-6
    * Users are prompted for the names of players in the game.  Names are checked to ensure they are unique
    * If player names unique, names are added into scores table & hand_total table
    * Session values are set to be referenced during the rest of the scoring session

* **@app.route("/score_house_items"):**
    * Prompts each player for their fleet_track position, helium count, influence count as well as who has the Sovereign Token
    * House items are totaled using total_house_items functions foun d in score_house_items.py.  Scoring is based on values assigned in board game rules. Reference house_details.py for details
    * Users can review totals before submitting

* **@app.route("/location_banished_record"):**
    * Prompts Users for relevant banished card counts as well as colors on all locations
    * Users need not enter values for every field, only the ones that will apply to their card's game end scoring.  Empty values will be set to 0
    * Inputs will be stored in location_banished_results table to be referenced by specific cards during the conditional scoring phase

* **@app.route("/add_cards"):**
    * Each player is given the option to click a button with each character card's name and color.  Clicking the card will add the card to the player's hand as recorded by the hand table
    * As cards are added to players' hands, the character card image will appear at the bottom of the screen to show the cards in hand
    * Each card can only be added by one player
    * If a card is clicked again, the card will be removed from the hand which would allow another player to add the card
    * Once all cards have been added to each player's hand, they can be submitted to calculate conditional points
    * More Session values are set to capture special cards that have game end scoring actions

* **app.route("/game_end_actions"):**
    * If the specific cards were in any players hand, additional prompts will be made
    * Gray cards will ask for an additional color to be added to hand which can help with other card's conditional point scoring
    * Orange cards will ask to change the name of this card to another card.  *Note that the name will be established as a "Ghost Card" and will not score the core or character's conditional points*
    * Hacker will prompt for the Core value of the top card of the deck
    * Developer will prompt for the Core value of any location

* **app.route("/hand_total"):**
    * Displays all cards in hand with final core & conditional points as well as card's point total
    * Once submitted, the house item scores, card count penalty, and hand totals will be calculate for each player
    * Users will be routed to a results page that will display the name of the game's winner


##### **Files in Project:**

* **database:** Database information used within application
    * **cards.csv:** The Original CSV file of character cards, used to create character_cards table in red_rising.db file
    * **red_rising.db:** Includes tables used in the scoring function of the app including:
        * scores - Tracks scores of all games
        * hand_total - Tracks sum of each players cards for current game
        * game_number - Keeps track of next game number to use
        * character_cards - Lists all character cards available for use in game along with character name, color, core points, conditions and conditional point values.
        * hand - Tracks cards in each player's hand during game and recorded values for each
        * location_banished_results - Tracks current games banished cards and location cards used for conditional scoring on some character cards

* **flask_session:** Stores Flask Session Information

* **functions:** Separate Python Functions used within app.py to call specific functions
    * **classes:** Includes folders for each Character Class/Color which include each card's individual scoring specifications
    * **conditions.py:** Creates a function map to map each character name to its relevant function name
    * **game_number.py:** Updates game number after each new game
    * **house_datils.py:** Used to calculate house items's scores
    * **location_banished.py:** Used to add location and banished values for game end scoring
    * **players.py:** Adds players to new game
    * **score_cards.py** Scores cards based on core and conditions
    * **score_house_items.py:** Gets house item counts and then runs house_details.py to calculate point values
    * **total_score.py:** Sums each players points and calculates winner

* **scripts:** Stores JavaScript file - *This file was not implemented as there was an error in implementing the Script unless directly placed in HTML file*

* **static:** Includes images and styling elements
    * **images:** Contains images used within the application, including 112 individual character cards
    * **styles.css:** The CSS file implemented in HTML pages

* **templates:** Includes HTML files for each page referenced within the routes found in app.py

* **app.py:**   This is the main Python file used by Flask to run the program

* **README.md:**    Summerizes this project

* **TODO_and_CODES.txt:** Details desired updates and snippets of code for reference


## Known Bugs
Although each card in the game has undergone testing to ensure that the expected results are produced, the limitless card combination possibilities mean that not every instance of a card's potential have been verified.  Users are encouraged to contact the developer if scoring errors occur.

## Licensing

[MIT](https://choosealicense.com/licenses/mit/) © Melissa Parker 2024
