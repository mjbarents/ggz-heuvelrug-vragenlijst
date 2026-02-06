from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets

db = SQLAlchemy()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    question_type = db.Column(db.String(20), nullable=False, default="scale")
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Question {self.id}: {self.text[:30]} ({self.question_type})>"


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    used_at = db.Column(db.DateTime, nullable=True)

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    def __repr__(self):
        return f"<Token {self.token[:10]}... used={self.used}>"


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(
        db.Integer, db.ForeignKey("token.id", ondelete="CASCADE"), nullable=False
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), nullable=False
    )
    score = db.Column(db.Integer, nullable=True)
    text_answer = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.now)

    token = db.relationship("Token", backref="responses")
    question = db.relationship("Question", backref="responses")

    def __repr__(self):
        if self.text_answer:
            return f"<Response token={self.token_id} question={self.question_id} text='{self.text_answer[:30]}'>"
        return f"<Response token={self.token_id} question={self.question_id} score={self.score}>"
