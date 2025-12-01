from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "database.db"

# 初始化資料庫
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)
        conn.commit()
        conn.close()

init_db()

# 寫資料到資料庫
def insert_score(game, name, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO scores (game, name, score) VALUES (?, ?, ?)", (game, name, score))
    conn.commit()
    conn.close()

# 取得遊戲排行榜
def get_top_scores(game, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores WHERE game = ? ORDER BY score DESC LIMIT ?", (game, limit))
    rows = c.fetchall()
    conn.close()
    return rows

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game1")
def game1():
    return render_template("game1.html")

@app.route("/game2")
def game2():
    return render_template("game2.html")

@app.route("/ranking")
def ranking():
    game = request.args.get("game", "game1")
    rows = get_top_scores(game)
    return render_template("ranking.html", game=game, rows=rows)

# 提交成績 API
@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.json
    game = data.get("game")
    score = int(data.get("score"))

    # 取得前10名成績
    top_scores = get_top_scores(game)

    # 如果沒滿10名，或成績大於第10名 → 有資格進榜
    eligible = False
    if len(top_scores) < 10:
        eligible = True
    elif score > top_scores[-1][1]:
        eligible = True

    # 若進榜需提供姓名
    if eligible:
        name = data.get("name")
        if name:  # 有提供姓名才寫入 DB
            insert_score(game, name, score)
        return jsonify({"eligible": True})
    else:
        return jsonify({"eligible": False})

if __name__ == "__main__":
    app.run(debug=True)
