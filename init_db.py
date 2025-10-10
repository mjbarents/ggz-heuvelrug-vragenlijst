from app import app, db
from models import Question


def init_database():
    with app.app_context():
        db.create_all()

        if Question.query.count() > 0:
            print("Database already initialized.")
            return

        standaard_vragen = [
            "Vind je jouw werk betekenisvol?",
            "Zit je met je werk in de flow?",
            "Voel je verbondenheid in het werk en het team?",
            "Voelt het werk als duurzaam?",
        ]

        for i, question_text in enumerate(standaard_vragen, start=1):
            question = Question(text=question_text, order=i)
            db.session.add(question)

        db.session.commit()
        print(f"Database successfully initialized")


if __name__ == "__main__":
    init_database()
