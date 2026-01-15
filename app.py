import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, send_from_directory
from flask_cors import CORS
from extensions import db
from models import User, VocabEntry, QuizRound, QuizAnswer, Card, UserCard
from routes.vocab import vocab_bp
from routes.quiz import quiz_bp
from routes.cards import cards_bp



def create_app():
    app = Flask(__name__)

    db_url = os.getenv('DATABASE_URL')  # Neon/Render!
    if db_url and 'neon.tech' in db_url:
        # Neon SSL + Format
        uri = db_url.replace('postgresql://', 'postgresql://')  # Schon OK
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
        print(f"✅ Neon Postgres: {uri.split('@')[1].split('/')[0]}")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///latin_vocab.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    # CORS für ALLE API + Frontend
    CORS(app, resources={
        r"/*": {
            "origins": "*",  # Oder ["https://aenigma-verborum-non-ai.onrender.com"]
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    # adds blueprints whose routes map directly to common operations on SQLite tables
    app.register_blueprint(vocab_bp, url_prefix="/api/vocab")
    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(cards_bp, url_prefix="/api/cards")

    with app.app_context():
        # ORM definitions turned into real SQLite tables before any API logic runs
        db.create_all()

    return app

app = create_app()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
