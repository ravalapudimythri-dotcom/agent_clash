from flask import Flask, render_template, request, redirect, session
import random

print("APP.PY IS RUNNING")

app = Flask(__name__)
app.secret_key = "agent_clash_secret"

ROUNDS = 5
START_RESOURCES = 100
MULTIPLIER = 1.5


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    if request.method == "POST":
        players = int(request.form["players"])

        session["players"] = players
        session["round"] = 1
        session["resources"] = [START_RESOURCES] * players
        session["scores"] = [0] * players

        return redirect("/game")

    return render_template("lobby.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    players = session.get("players")

    if players is None:
        return redirect("/")

    if request.method == "POST":
        pool = 0

        for i in range(players):
            c = int(request.form.get(f"p{i}", 0))
            c = max(0, min(c, session["resources"][i]))

            session["resources"][i] -= c
            pool += c

        pool = int(pool * MULTIPLIER)
        share = pool // players

        for i in range(players):
            session["resources"][i] += share
            session["scores"][i] += session["resources"][i]

        session["round"] += 1

        if session["round"] > ROUNDS:
            return redirect("/result")

    return render_template(
        "game.html",
        round=session["round"],
        resources=session["resources"]
    )


@app.route("/result")
def result():
    scores = session.get("scores", [])
    winner = scores.index(max(scores)) + 1 if scores else None

    return render_template("result.html", scores=scores, winner=winner)


if __name__ == "__main__":
    app.run(debug=True)