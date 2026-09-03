from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_FILE = "notes.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, content FROM notes")
    notes = [{"id": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(notes), 200


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "content field is required"}), 400
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("INSERT INTO notes (content) VALUES (?)", (data["content"],))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": note_id, "content": data["content"]}), 201


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"note {note_id} deleted"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
