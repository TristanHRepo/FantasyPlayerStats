from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

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
        player1 = players[0]
        player1 = player1.rsplit(" ")
        player2 = players[1]
        player2 = player2.rsplit(" ")

        # Create url's for Jon's Service
        service_url1 = "http://35.209.40.140/v1/players/"
        service_url1 = service_url1 + player1[0] + " " + player1[1]
        service_url2 = "http://35.209.40.140/v1/players/"
        service_url2 = service_url2 + player2[0] + " " + player2[1]
        data1 = requests.get(service_url1)
        data1 = data1.json()
        data2 = requests.get(service_url2)
        data2 = data2.json()

        espn_url1 = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/"
        espn_url1 = espn_url1 + data1['espn_id']
        espn_data1 = requests.get(espn_url1)
        espn_data1 = espn_data1.json()
        espn_url2 = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/"
        espn_url2 = espn_url2 + data2['espn_id']
        espn_data2 = requests.get(espn_url2)
        espn_data2 = espn_data2.json()

        data1['age'] = espn_data1['athlete']['age']
        data1['draft'] = espn_data1['athlete']['displayDraft']
        for item in espn_data1['athlete']['statsSummary']['statistics']:
            data1[item['name']] = item['value']
        logo = espn_data1['athlete']['team']['logos'][0]['href']
        logo_color = espn_data1['athlete']['team']['color']
        data1['logo'] = logo
        data1['logo_color'] = "#" + logo_color + "E5"

        data2['age'] = espn_data2['athlete']['age']
        data2['draft'] = espn_data2['athlete']['displayDraft']
        for item in espn_data2['athlete']['statsSummary']['statistics']:
            data2[item['name']] = item['value']
        logo = espn_data2['athlete']['team']['logos'][0]['href']
        logo_color = espn_data2['athlete']['team']['color']
        data2['logo'] = logo
        data2['logo_color'] = "#" + logo_color + "E5"
        
        return render_template('comparison.html', player1=data1, player2=data2)

    return render_template('index.html')


@app.route('/tools/profile', methods=['POST'])
def playerStats():
    # POST to get a players stats and display them in their profile
    if request.form['function'] == 'Profile':

        """ USE THIS TO GET DATA LATER: https://stackoverflow.com/questions/65323857/trying-to-scrape-data-from-pro-football-reference"""

        # Get player name from form
        player = request.form['player']
        player = player.rsplit(" ")

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

        # Add data to the data already available
        jon_data['age'] = espn_data['athlete']['age']
        jon_data['draft'] = espn_data['athlete']['displayDraft']
        for item in espn_data['athlete']['statsSummary']['statistics']:
            jon_data[item['name']] = item['value']
        logo = espn_data['athlete']['team']['logos'][0]['href']
        logo_color = espn_data['athlete']['team']['color']
        jon_data['logo'] = logo
        jon_data['logo_color'] = "#" + logo_color + "E5"

        # load page based on the player's position
        if jon_data['position'] == 'QB':
            return render_template('statsQB.html', data=jon_data)
        elif jon_data['position'] == 'RB':
            return render_template('statsRB.html', data=jon_data)
        elif jon_data['position'] == 'WR':
            return render_template('statsWR.html', data=jon_data)
        elif jon_data['position'] == 'TE':
            return render_template('statsTE.html', data=jon_data)

    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7777))
    app.run(port=port, debug=True)
