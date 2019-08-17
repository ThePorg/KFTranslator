from flask import Flask, redirect, render_template, request, url_for, send_file
import requests
import json
import subprocess

app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")

    create_printout(request.form["contents"])
    subprocess.check_call(['pdflatex', 'decklist.tex'])
    try:
        return send_file('decklist.pdf')
    except Exception as e:
        return str(e)

def create_printout(url):
    deckobj = get_deck_from_url(url)
    generate_file(deckobj)

def get_deck_from_url(url):
    deck_id = url.split("/")[-1]
    deck_url = 'https://www.keyforgegame.com/api/decks/' + deck_id.strip() + '/?links=cards'
    deck_page = requests.get(deck_url, headers = {'Accept-Language': 'fr', 'links': 'cards'})
    return json.loads(deck_page.text)

def generate_file(deck):
    name = deck.get("data").get("name")
    houses = deck.get("data").get("_links").get("houses")
    card_index = deck.get("data").get("_links").get("cards")
    card_data = deck.get("_linked").get("cards")
    cards = get_card_list(card_index, card_data)
    make_tex(name, houses, cards)

def get_card_list(index, data):
    deck = []
    for id in index:
        deck.append(get_card_name(data, id))
    return deck

def get_card_name(data, id):
    for i in range (len(data)):
        if data[i].get("id") == id:
            card = data[i].get("card_number") + " " + data[i].get("card_title") + "\\\\"
            return card.replace("}", "")
    return "error"

def make_tex(name, houses, cards):
    file = "\\documentclass[11pt]{scrartcl} \n" + "\\usepackage[utf8]{inputenc} \n"\
           "\\usepackage[T1]{fontenc} \n" + "\\usepackage[margin=0pt, landscape]{geometry} \n"\
           "\\usepackage{graphicx} \n" + "\\usepackage{color} \n" + "\\definecolor{mygray}{gray}{.75} \n"\
           "\\usepackage{url} \n" + "\\usepackage[colorlinks=false, pdftitle={Decklist},"\
           "pdfauthor={Admiral Deathrain},pdfsubject={International KeyForge Decklist},"\
           "pdfkeywords={KeyForge, Decklist}]{hyperref} \n" + "\\setlength{\\unitlength}{1mm} \n"\
           "\\setlength{\\parindent}{0pt} \n" + "\\newcommand{\\sectiontitle}[1]{\\paragraph{#1}\\ \\\\} \n"\
           "\\begin{document}\n" + "\\begin{picture}(297,210)\n" + "\\put(10,200){\n"\
           "\\begin{minipage}[t]{210mm}\n" + "\\section*{" + name + "}\n" + "\\end{minipage}\n" + "} \n"\
           "\\put(10,180){\n" + "\\begin{minipage}[t]{85mm} \n" + "\\sectiontitle{" + houses[0] + "}"\
           " " + "".join(cards[0:12]) + "\\sectiontitle{" + houses[1] + "} \n" + "".join(cards[12:24]) + "\\end{minipage} \n }"\
           "\\put(105,180){\n" + "\\begin{minipage}[t]{85mm}" + "\\sectiontitle{" + houses[2] + "}"\
           " " + "".join(cards[24:36]) + "\\end{minipage} \n" + "} \n" + "\\put(200,180){ \n" + "\\begin{minipage}[t]{85mm}"\
           " \n \\end{minipage} \n } \n" + "\\end{picture} \n" + "\\end{document}"
    texfile = open("decklist.tex", "w")
    texfile.write(file)
    texfile.close()
