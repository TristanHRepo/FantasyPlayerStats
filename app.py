from flask import Flask, render_template, redirect, request
import os

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/tools', methods=['POST'])
def playerStats():
    # POST to compare two or more players
    if request.form['function'] == 'compare':
        return render_template('comparison.html')

    # POST to get a players stats and display them in their profile
    elif request.form['function'] == 'profile':
        return render_template('stats.html')

    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7777))
    app.run(port=port, debug=True)