from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500))
    bot_response = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Jalankan hanya jika file ini langsung dijalankan
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database & tabel berhasil dibuat.")

