from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import csv
import os
import io

app = Flask(__name__)
CORS(app)
app.secret_key = "rahasia-super-unik-123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faq.db'
db = SQLAlchemy(app)

@app.route('/healthz')
def healthz():
    return "OK"

# Models
class ChatbotResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(300), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Chat Logic
def find_closest_question(user_input, threshold=0.3):
    responses = ChatbotResponse.query.all()
    if not responses:
        return "Maaf, saya belum memiliki cukup data."

    questions = [resp.question for resp in responses]
    answers = [resp.answer for resp in responses]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(questions + [user_input])
    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    max_sim = similarity.max()

    if max_sim < threshold:
        return "Maaf, saya belum mengerti pertanyaan tersebut."

    idx = similarity.argmax()
    return answers[idx]

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'new_question' in request.form and 'new_answer' in request.form:
            question = request.form['new_question']
            answer = request.form['new_answer']
            if not ChatbotResponse.query.filter_by(question=question).first():
                new_data = ChatbotResponse(question=question, answer=answer)
                db.session.add(new_data)
                db.session.commit()
                flash("FAQ berhasil ditambahkan.", "success")
            else:
                flash("Pertanyaan sudah ada!", "warning")
    all_data = ChatbotResponse.query.all()
    return render_template("index.html", data=all_data)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message") or request.json.get("message")
    bot_response = find_closest_question(user_message)

    history = ChatHistory(user_message=user_message, bot_response=bot_response)
    db.session.add(history)
    db.session.commit()

    return jsonify({"response": bot_response})

@app.route('/add', methods=['POST'])
def add_faq():
    question = request.form['new_question']
    answer = request.form['new_answer']
    if not ChatbotResponse.query.filter_by(question=question).first():
        new_data = ChatbotResponse(question=question, answer=answer)
        db.session.add(new_data)
        db.session.commit()
        flash("FAQ berhasil ditambahkan.", "success")
    else:
        flash("Pertanyaan sudah ada!", "warning")
    return redirect(url_for('index'))

@app.route("/history")
def history():
    chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).all()
    return render_template("history.html", chats=chats)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["csv_file"]
    if file and file.filename.endswith(".csv"):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        added = 0
        skipped = 0
        for row in csv_input:
            if len(row) == 2:
                question, answer = row
                if not ChatbotResponse.query.filter_by(question=question).first():
                    db.session.add(ChatbotResponse(question=question, answer=answer))
                    added += 1
                else:
                    skipped += 1
        db.session.commit()
        flash(f"{added} data berhasil ditambahkan. {skipped} dilewati karena duplikat.", "success")
    else:
        flash("Format file tidak valid. Harus .csv", "danger")
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_faq(id):
    faq = ChatbotResponse.query.get_or_404(id)
    if request.method == "POST":
        faq.question = request.form["question"]
        faq.answer = request.form["answer"]
        db.session.commit()
        flash("FAQ berhasil diperbarui!", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", faq=faq)

@app.route("/delete/<int:id>")
def delete_faq(id):
    faq = ChatbotResponse.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash("FAQ berhasil dihapus!", "warning")
    return redirect(url_for("index"))

@app.route('/update_faq/<int:id>', methods=['POST'])
def update_faq(id):
    faq = ChatbotResponse.query.get_or_404(id)
    faq.question = request.form['question']
    faq.answer = request.form['answer']
    db.session.commit()
    flash('FAQ berhasil diperbarui!', 'success')
    return redirect(url_for('index'))

@app.route("/chat_ui")
def chat_ui():
    return render_template("user_chat.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get('PORT', 5000))  # Ambil PORT dari environment Railway
    app.run(host='0.0.0.0', port=port, debug=True)  # Listen ke semua IP (0.0.0.0) dan pakai port Railway