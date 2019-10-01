# KFTranslator
Tiny app for creating international keyforge decklist printouts to help with tournament communication.
To host it you need Python3.7 with Flask and Requests and a LaTeX distribution with XeLaTeX included.
When hosting locally, change "return send_file('../../decklist.pdf')" in line 19 of app.py to 
"return send_file('decklist.pdf')"
