from flask import Flask, render_template, redirect, request
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
        data = ["24", "6'11\"", "214 lbs", "LSU", "1st Round", "2", "5", "5", "0", "433", "488", "-55", "38", "41", "-3", "53", "48", "+5", "4", "3", "+1"]
        return render_template('stats.html', player=player, data=data)

    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7777))
    app.run(port=port, debug=True)
