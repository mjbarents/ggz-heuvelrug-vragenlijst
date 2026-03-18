from app import app, db
from models import Question
from db_migrations import run_schema_migrations


def init_database():
    with app.app_context():
        db.create_all()
        run_schema_migrations()

        if Question.query.count() > 0:
            print("Database already initialized.")
            return

        standaard_vragen = [
            ("Vind je jouw werk betekenisvol?", "scale"),
            ("Zit je met je werk in de flow?", "scale"),
            ("Voel je verbondenheid in het werk en het team?", "scale"),
            ("Voelt het werk als duurzaam?", "scale"),
            ("Heb je nog overige opmerkingen die je zou willen toevoegen?", "open"),
        ]

        for i, (question_text, question_type) in enumerate(standaard_vragen, start=1):
            question = Question(text=question_text, order=i, question_type=question_type)
            db.session.add(question)

        db.session.commit()
        print(f"Database successfully initialized")


if __name__ == "__main__":
    init_database()
