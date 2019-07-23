from flask import Flask, redirect, render_template, request, url_for



app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")

    comment = Comment(content=request.form["contents"])
    return redirect(url_for('index'))
