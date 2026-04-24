from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "rp-secret"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        subject TEXT,
        grade INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT subject, grade FROM grades WHERE user=?", (user,))
    data = c.fetchall()
    conn.close()

    return render_template("dashboard.html", user=user, grades=data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ("PORT", 5000)))
