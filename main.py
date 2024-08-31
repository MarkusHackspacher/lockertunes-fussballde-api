#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for
from fussballdescraper import get_teams, get_matches
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def format_url(url: str) -> str:
    url = 'https://www.fussball.de/' + url
    url = url.replace('SLASH', '/')
    return url + '#!/'


def format_team_name(team_name: str) -> str:
    return team_name.replace('SPACE', ' ')


@app.route('/get-teams/<string:league_url>', methods=['GET'])
def request_teams(league_url: str):
    url = format_url(league_url)
    return jsonify(get_teams(url)), 201


@app.route('/get-matches/<string:team_name>/<string:league_url>/<int:game_span>', methods=['GET'])
def request_matches(team_name: str, league_url: str, game_span: int):
    team_name = format_team_name(team_name)
    league_url = format_url(league_url)
    matches_dict = []
    matches = get_matches(team_name, league_url, game_span)
    for match in matches:
        matches_dict.append(match.to_dict())

    return jsonify(matches_dict), 202


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  

        url = request.form['url']
        return redirect(url_for('second_gui', url=url))
    return render_template('index.html')

@app.route('/second_gui', methods=['GET', 'POST'])
def second_gui():
    url = request.args.get('url')
    teams = get_teams(url)
    if request.method == 'POST':
        selected_team = request.form['team']
        return redirect(url_for('third_gui', url=url, selected_team=selected_team))

    return render_template('second_gui.html', url=url, teams=teams)

@app.route('/third_gui', methods=['GET', 'POST'])
def third_gui():
    url = request.args.get('url')
    selected_team = request.args.get('selected_team')
    if selected_team:
        matches = get_matches(selected_team, url, 50)
        matches_dict = []
        for match in matches:
            matches_dict.append(match.to_dict())
        if request.method == 'POST': 
            return jsonify(matches_dict), 202
        return render_template('third_gui.html', matches=matches, url=url)
    return "Keine Daten ausgewählt."

if __name__ == '__main__':
    app.run(debug=True)
