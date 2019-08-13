from flask import Flask, redirect, render_template, request, url_for, send_file
import requests
import json

app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")

    create_printout(request.form["contents"])
    try:
        return send_file('LICENSE')
    except Exception as e:
        return str(e)

def create_printout(url):
    deck = get_deck_from_url(url)
    generate_file(deck)

def get_deck_from_url(url):
    deck_id = url.split("/")[-1]
    deck_url = 'https://www.keyforgegame.com/api/decks/' + deck_id.strip() + '/?links=cards'
    deck_page = requests.get(deck_url)
    return json.loads(deck_page)

def generate_file(deck):
    name = deck.get("data").get("name")
    houses = deck.get("data").get("_links").get("houses")
    card_index = deck.get("data").get("_links").get("cards")
    card_data = deck.get("_linked").get("cards")
