# import app variable from init file from the app directory
from app import app
from web_scraping import *


from flask import render_template, request

# this function runs when a person enters this URL on the website
## render_template will render the site in the html format specified by the index.html file
@app.route("/", methods = ["GET", "POST"])
def index():

    if request.method == "POST":
        get_player_stats()
        get_team_stats()
        clean_data()

    return render_template("index.html")

@app.route("/results", methods = ["GET", "POST"])
def results():

    top_10 = []

    if request.method == "POST":

        top_10 = ['Giannis Antetokounmpo', 'Luka Dončić', 'Joel Embiid', 'Nikola Jokić',
            'Anthony Davis', 'Kevin Durant', 'Jayson Tatum', 'Shai Gilgeous-Alexander',
            'LeBron James', 'Stephen Curry']
        print(top_10)

        return render_template("results.html", top_10 = top_10)

    return render_template("results.html")