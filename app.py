from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Route to show all notes
@app.route("/")
def index():
    notes = Note.query.all()
    return render_template("index.html", notes=notes)

# Route to add a new note
@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content")
    if content:
        new_note = Note(content=content)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for("index"))

# ✅ Route to edit a note
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        note.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", note=note)

# Route to delete a note
@app.route("/delete/<int:id>")
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
