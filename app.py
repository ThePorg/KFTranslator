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
        return send_file('../../decklist.pdf')
    except Exception as e:
        return str(e)

#Retrieve all deck objects and generate the .tex file
def create_printout(url):
    langs = ['en', 'de', 'es', 'fr', 'it', 'pl', 'pt', 'zh']
    decks = []
    for lang in langs:
        deck = get_deck_from_url(url, lang)
        decks.append(deck)
    generate_file(decks)

#Return .json deck object from Asmodees website in the languages required
def get_deck_from_url(url, lang):
    deck_id = url.split("/")[-1].partition('?')[0]
    deck_url = 'https://www.keyforgegame.com/api/decks/' + deck_id.strip() + '/?links=cards'
    deck_page = requests.get(deck_url, headers = {'Accept-Language': lang, 'links': 'cards'})
    return json.loads(deck_page.text)

#Prepare the deck data to be turned into a .tex file
def generate_file(decks):
    cardlists = []
    for deck in decks:
        card_index = deck.get("data").get("_links").get("cards")
        card_data = deck.get("_linked").get("cards")
        cards = get_card_list(card_index, card_data)
        cardlists.append(cards)
    name = decks[0].get("data").get("name")
    houselists = []
    for deck in decks:
        houses = deck.get("data").get("_links").get("houses")
        houselists.append(houses)
    make_tex(name, houselists, cardlists)

#Return a list of strings with a card list using the index provided by the .json so cards are in the correct order
def get_card_list(index, data):
    deck = []
    for id in index:
        deck.append(get_card_name(data, id))
    return deck

#Return a cards text and number and a LaTeX linebreak
def get_card_name(data, id):
    for i in range (len(data)):
        if data[i].get("id") == id:
            card = data[i].get("card_number") + " " + data[i].get("card_title") + "\\\\"
            return card
    return "error"

#Build a .tex file and write it
def make_tex(name, houselists, cardlists):
    content = write_content(houselists, cardlists)
    file = "\\documentclass[10pt]{report} \n" + "\\usepackage[utf8]{inputenc} \n" + "\\usepackage{multicol} \n" + "\\usepackage{CJKutf8} \n"\
           "\\usepackage[T1]{fontenc} \n" + "\\usepackage[a4paper, landscape, margin=.5in]{geometry} \n"\
           "\\usepackage{url} \n" + "\\usepackage[colorlinks=false, pdftitle={Decklist},"\
           "pdfauthor={Admiral Deathrain},pdfsubject={International KeyForge Decklist},"\
           "pdfkeywords={KeyForge, Decklist}]{hyperref} \n" + "\\setlength{\\unitlength}{1mm} \n"\
           "\\setlength{\\parindent}{0pt} \n" + "\\newcommand{\\sectiontitle}[1]{\\paragraph{#1}\\ \\\\} \n"\
           "\\begin{document}\n \\begin{CJK}{UTF8}{bsmi}\n" + "\\section*{" + name + "}\n" + "\\begin{multicols*}{5}"  + content + " "\
           "\\\\ \n Created with KFTranslator:" + "\\\\ \n deathrain.pythonanywhere.com " + " \n \\end{multicols*} " + "\n \\end{CJK} \n \\end{document}"

    texfile = open("decklist.tex", "w")
    texfile.write(file)
    texfile.close()

#Create conjoined content string
def write_content(houselists, cardlists):
    content = ""
    for i in range (len(houselists)):
            content = content + "\\sectiontitle{" + houselists[i][0] + "} \n"\
                      " " + "".join(cardlists[i][0:12]) + "\n"\
                      " " + "\\sectiontitle{" + houselists[i][1] + "} \n"\
                      " " + "".join(cardlists[i][12:24]) + "\n"\
                      " " + "\\sectiontitle{" + houselists[i][2] + "} \n"\
                      " " + "".join(cardlists[i][24:36]) + "\n"\
                      "\\rule{.18\\textwidth}{1pt}"
    return content

