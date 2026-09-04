import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "cloudnotesdb")
DB_USER = os.environ.get("DB_USER", "cloudnotes")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "devpassword123")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM notes")
    notes = [{"id": row[0], "content": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(notes), 200


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "content field is required"}), 400
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s) RETURNING id", (data["content"],))
    note_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": note_id, "content": data["content"]}), 201


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"note {note_id} deleted"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
