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

        return render_template('comparison.html', players=players, data=data)

    return render_template('index.html')


@app.route('/tools/profile', methods=['POST'])
def playerStats():
    # POST to get a players stats and display them in their profile
    if request.form['function'] == 'Profile':
        player = request.form['player']
        player = player.rsplit(" ")
        service_url = "http://35.209.40.140/v1/players/"
        service_url = service_url + player[0] + " " + player[1]
        jon_data = requests.get(service_url)
        jon_data = jon_data.json()

        espn_url = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/"
        espn_url = espn_url + jon_data['espn_id']
        espn_data = requests.get(espn_url)
        espn_data = espn_data.json()

        jon_data['age'] = espn_data['athlete']['age']
        jon_data['draft'] = espn_data['athlete']['displayDraft']
        for item in espn_data['athlete']['statsSummary']['statistics']:
            jon_data[item['name']] = item['value']

        print(jon_data)
        return render_template('stats.html', data=jon_data)

    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7777))
    app.run(port=port, debug=True)
