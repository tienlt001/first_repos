from flask import Flask, render_template, request, jsonify, session
from .game import Board
from .ai import best_move

app = Flask(__name__, template_folder="templates", static_folder="static")
# NOTE: For development only. Use a secure key in production.
app.secret_key = "dev-secret"


def _state():
    cells = session.get("cells", [" "] * 9)
    current = session.get("current", "X")
    b = Board()
    b.cells = cells
    return {
        "cells": cells,
        "current": current,
        "winner": "X" if b.is_winner("X") else ("O" if b.is_winner("O") else None),
        "draw": b.is_draw(),
    }


@app.route("/")
def index():
    s = _state()
    return render_template("index.html", cells=s["cells"], current=s["current"], winner=s["winner"], draw=s["draw"])


@app.route("/state")
def state():
    return jsonify(_state())


@app.route("/new", methods=["POST"])
def new_game():
    data = request.get_json() or {}
    session["cells"] = [" "] * 9
    session["current"] = "X"
    session["ai_enabled"] = bool(data.get("ai_enabled", True))
    session["ai_player"] = data.get("ai_player", "O")
    # If AI is X and starts, let it make a move immediately
    if session["ai_enabled"] and session["ai_player"] == "X":
        b = Board()
        b.cells = session["cells"]
        m = best_move(b, session["ai_player"])
        if m != -1:
            b.make_move(m, session["ai_player"])
            session["cells"] = b.cells
            session["current"] = "O"
    return jsonify(success=True, **_state())


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json() or {}
    idx = data.get("index")
    if not isinstance(idx, int) or not (0 <= idx < 9):
        return jsonify(success=False, error="invalid index"), 400

    cells = session.get("cells", [" "] * 9)
    current = session.get("current", "X")
    ai_enabled = session.get("ai_enabled", True)
    ai_player = session.get("ai_player", "O")

    if cells[idx] != " ":
        return jsonify(success=False, error="cell occupied", **_state()), 400

    cells[idx] = current
    session["cells"] = cells

    b = Board()
    b.cells = cells
    if b.is_winner(current):
        return jsonify(success=True, winner=current, **_state())
    if b.is_draw():
        return jsonify(success=True, draw=True, **_state())

    # switch
    current = "O" if current == "X" else "X"
    session["current"] = current

    # If AI's turn, let it play
    if ai_enabled and current == ai_player:
        m = best_move(b, ai_player)
        if m != -1:
            b.make_move(m, ai_player)
            session["cells"] = b.cells
        if b.is_winner(ai_player):
            return jsonify(success=True, winner=ai_player, **_state())
        if b.is_draw():
            return jsonify(success=True, draw=True, **_state())
        # switch back
        session["current"] = "O" if current == "X" else "X"

    return jsonify(success=True, **_state())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
