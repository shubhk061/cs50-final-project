from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from secrets import token_urlsafe
from groq import Groq
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
app.secret_key = "your-secret-key"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_db():
    db = sqlite3.connect("project/project.db")
    db.row_factory = sqlite3.Row
    return db


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not email:
            return "email required"
        if not password:
            return "password required"
        if password != confirmation:
            return "Password do not match"

        db = get_db()
        hash = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (email, hash) VALUES (?, ?)",
            (email, hash)
        )

        db.commit()
        db.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            return "email required"

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if not user:
            db.close()
            return "Email not found"

        token = token_urlsafe(32)

        db.execute(
            """
            INSERT INTO password_resets (user_id, token, expires_at)
            VALUES (?, ?, ?)
            """,
            (user["id"], token, 999999999)
        )

        db.commit()
        db.close()

        reset_link = f"/reset_password/{token}"

        return f'<a href="{reset_link}">Click here to reset your password</a>'

    return render_template("password.html")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):

    db = get_db()

    reset = db.execute(
        "SELECT * FROM password_resets WHERE token = ?",
        (token,)
    ).fetchone()

    if not reset:
        db.close()
        return "Invalid reset link"

    if request.method == "POST":

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password:
            db.close()
            return "Password required"

        if password != confirmation:
            db.close()
            return "Passwords do not match"

        hash = generate_password_hash(password)

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            (hash, reset["user_id"])
        )

        db.execute(
            "DELETE FROM password_resets WHERE token = ?",
            (token,)
        )

        db.commit()
        db.close()

        return redirect("/login")

    db.close()
    return render_template("reset.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            return "email not exist"
        if not password:
            return "password not exist"

        db = get_db()

        rows = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchall()

        db.close()

        if len(rows) != 1:
            return "Invlaid email or password"
        if not check_password_hash(rows[0]["hash"], password):
            return "Invalid email or password"

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/ask", methods=["POST"])
def ask():
    if "user_id" not in session:
        return redirect("/login")

    question = request.form.get("question")

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content

        answer_html = markdown.markdown(
            answer,
            extensions=["tables", "fenced_code"]
        )

        db = get_db()

        db.execute(
            """
            INSERT INTO conversations (user_id, question, answer)
            VALUES (?, ?, ?)
            """,
            (session["user_id"], question, answer)
        )

        db.commit()
        db.close()

    except Exception as e:

        print("ERROR:", e)
        answer = "Sorry, the AI service is temporarily unavailable."
        answer_html = markdown.markdown(answer)

    db = get_db()

    conversations = db.execute(
        """
        SELECT id, question, answer
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template(
        "index.html",
        answer=answer_html,
        question=question,
        conversations=conversations
    )


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    conversations = db.execute(
        """
        SELECT question, answer
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()
    return render_template("history.html", conversations=conversations)


@app.route("/clear_history", methods=["POST"])
def clear_history():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    db.execute(
        "DELETE FROM conversations WHERE user_id = ?",
        (session["user_id"],)
    )

    db.commit()
    db.close()

    return redirect("/history")


@app.route("/conversation/<int:conversation_id>")
def conversation(conversation_id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    conversation = db.execute(
        """
        SELECT question, answer
        FROM conversations
        WHERE id = ? AND user_id = ?
        """,
        (conversation_id, session["user_id"])
    ).fetchone()

    db.close()

    if not conversation:
        return "Conversation not found"
    answer_html = markdown.markdown(
        conversation["answer"],
        extensions=["tables", "fenced_code"]
    )

    return render_template(

       "index.html",
        answer=answer_html,
        question=conversation["question"]
)


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    conversations = db.execute(
        """
        SELECT id, question, answer
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template(
        "index.html",
        conversations=conversations
    )


if __name__ == "__main__":
    app.run(debug=True)
