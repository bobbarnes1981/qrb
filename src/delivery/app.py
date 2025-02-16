from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route("/candidatetest/<int:candidatetest_id>")
def delivery(candidatetest_id):
    return render_template("candidatetest.html", candidatetest_id=candidatetest_id)
