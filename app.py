from flask import Flask, render_template, request, redirect, url_for, session
from database import get_connection, create_tables

app = Flask(__name__)

# Secret key for login sessions
app.secret_key = "smart_library_secret_key"

# Create database tables
create_tables()


# Home page
@app.route("/")
def home():
    return redirect(url_for("login"))


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except Exception:
            conn.close()
            return "Username already exists!"

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))

        return "Invalid username or password!"

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# Books page
@app.route("/books")
def books():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    books = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    conn.close()

    return render_template(
        "books.html",
        books=books
    )


# Simple AI book recommendation
@app.route("/recommend", methods=["POST"])
def recommend():

    if "username" not in session:
        return redirect(url_for("login"))

    category = request.form["category"]

    conn = get_connection()

    recommendations = conn.execute(
        "SELECT * FROM books WHERE category = ?",
        (category,)
    ).fetchall()

    conn.close()

    return render_template(
        "books.html",
        books=recommendations,
        recommendation=True
    )


# Logout
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)