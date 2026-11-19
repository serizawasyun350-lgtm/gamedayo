from flask import Flask, render_template, redirect, url_for, jsonify, request

app = Flask(__name__)

# サーバー側インメモリランキング（デモ用初期データ）
LEADERBOARD = [
    {"name": "CYBER_ACE", "rank": "💎 ダイヤモンドランク", "score": 1250000, "kills": 3200},
    {"name": "STAR_HUNTER", "rank": "💠 プラチナランク", "score": 480000, "kills": 1150},
    {"name": "NEON_ROOKIE", "rank": "🥇 ゴールドランク", "score": 120000, "kills": 340},
]

DIFFICULTIES = {
    "easy": {"label": "🟢 EASY (かんたん)", "enemyHp": 0.6, "enemySpeed": 0.75, "playerDmgTaken": 0.5, "rewardMult": 0.8},
    "normal": {"label": "🔵 NORMAL (ふつう)", "enemyHp": 1.0, "enemySpeed": 1.0, "playerDmgTaken": 1.0, "rewardMult": 1.0},
    "hard": {"label": "🟠 HARD (むずかしい)", "enemyHp": 1.6, "enemySpeed": 1.3, "playerDmgTaken": 1.4, "rewardMult": 2.0},
    "nightmare": {"label": "🔴 NIGHTMARE (悪夢)", "enemyHp": 3.0, "enemySpeed": 1.65, "playerDmgTaken": 2.0, "rewardMult": 5.0},
    "god": {"label": "🟣 GOD (超神級インフレ)", "enemyHp": 10.0, "enemySpeed": 2.0, "playerDmgTaken": 3.0, "rewardMult": 25.0},
}


@app.route("/")
def root():
    return redirect(url_for("home_page"))


@app.route("/home")
def home_page():
    return render_template("index.html", initial_route="home")


@app.route("/game")
def game_page():
    return render_template("index.html", initial_route="game")


@app.route("/shop")
def shop_page():
    return render_template("index.html", initial_route="shop")


@app.route("/ranking")
def ranking_page():
    return render_template("index.html", initial_route="ranking")


@app.route("/settings")
def settings_page():
    return render_template("index.html", initial_route="settings")


@app.route("/api/difficulties")
def api_difficulties():
    return jsonify(DIFFICULTIES)


@app.route("/api/ranking", methods=["GET", "POST"])
def api_ranking():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "PILOT"))[:16]
        rank = str(data.get("rank", "🔰 ルーキーランク"))
        score = int(data.get("score", 0))
        kills = int(data.get("kills", 0))

        # 既存プレイヤー更新または新規追加
        existing = next((r for r in LEADERBOARD if r["name"] == name), None)
        if existing:
            existing["score"] = max(existing["score"], score)
            existing["kills"] = max(existing["kills"], kills)
            existing["rank"] = rank
        else:
            LEADERBOARD.append({"name": name, "rank": rank, "score": score, "kills": kills})

        LEADERBOARD.sort(key=lambda x: x["score"], reverse=True)
        return jsonify({"status": "ok", "leaderboard": LEADERBOARD[:10]})

    return jsonify({"leaderboard": LEADERBOARD[:10]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
