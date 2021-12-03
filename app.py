from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)


def format_espn_data(data):
    """Formats all the stats into a format usable for the html/css code"""

    stats = {}

    for stat in range(len(data['names'])):
        compiled_data = []
        if data['names'][stat] == 'fumblesForced' or data['names'][stat] == 'kicksBlocked':
            continue
        for game in data['seasonTypes'][0]['categories'][0]['events']:
            compiled_data.append(float(game['stats'][stat]))

        stats[data['names'][stat]] = compiled_data
    return stats


def get_player_data(player):
    """Gets the data for a player that is relevant to this application using Jon Baird's api and espn's api"""

    # Create url for Jon's Service
    service_url = "http://35.209.40.140/v1/players/"
    service_url = service_url + player[0] + " " + player[1]
    jon_data = requests.get(service_url)
    jon_data = jon_data.json()

    # Get extra data based on data from Jon's service
    espn_url = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/"
    espn_url = espn_url + jon_data['espn_id']
    espn_data = requests.get(espn_url)
    espn_data = espn_data.json()

    # Player per game stats and totals
    espn_url = espn_url + "/gamelog"
    pgStats = requests.get(espn_url)
    pgStats = pgStats.json()
    stats = format_espn_data(pgStats)
    jon_data['displayNames'] = pgStats['displayNames']
    jon_data['abbreviations'] = pgStats['labels']
    jon_data['totals'] = pgStats['seasonTypes'][0]['summary']['stats'][0]['stats']
    if jon_data['position'] != 'QB':
        jon_data['displayNames'].remove('Forced Fumbles')
        jon_data['displayNames'].remove('Kicks Blocked')
        jon_data['abbreviations'].remove('FF')
        jon_data['abbreviations'].remove('KB')

    # Add data to the data already available
    jon_data['age'] = espn_data['athlete']['age']
    jon_data['draft'] = espn_data['athlete']['displayDraft']
    logo = espn_data['athlete']['team']['logos'][0]['href']
    logo_color = espn_data['athlete']['team']['color']
    jon_data['logo'] = logo
    jon_data['logo_color'] = "#" + logo_color + "E5"

    jon_data['gameStats'] = stats

    return jon_data


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/tools/comparison', methods=['POST'])
def playerComparison():
    # POST to compare two or more players
    if request.form['function'] == 'Compare':
        players = []
        data = {}
        for item in request.form:
            if item == 'function':
                continue
            player = request.form[item]
            players.append(player)
            data[player] = []

        # Get players names
        player1 = players[0].rsplit(" ")
        player2 = players[1].rsplit(" ")

        data1 = get_player_data(player1)
        data2 = get_player_data(player2)

        return render_template('comparison.html', player1=data1, player2=data2)

    return render_template('index.html')


@app.route('/tools/profile', methods=['POST'])
def playerStats():
    # POST to get a players stats and display them in their profile
    if request.form['function'] == 'Profile':

        # Get player name from form
        player = request.form['player']
        player = player.rsplit(" ")

        data = get_player_data(player)

        # load page based on the player's position
        return render_template('stats.html', data=data)

    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7777))
    app.run(port=port, debug=True)
