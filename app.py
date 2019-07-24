from flask import Flask, redirect, render_template, request, url_for, send_file
import requests
import json

app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")

    return get_deck_from_url(request.form["contents"])
    try:
        return send_file('LICENSE')
    except Exception as e:
        return str(e)

def create_printout(url):
    deck = get_deck_from_url(url)

def get_deck_from_url(url):
    deck_id = url.split("/")[-1]
    deck_url = 'https://www.keyforgegame.com/api/decks/' + deck_id.strip() + '/?links=cards'
    deck_page = requests.get(deck_url)
    return str(deck_page.json())
