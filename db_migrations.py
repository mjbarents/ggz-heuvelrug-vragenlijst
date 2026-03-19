from datetime import datetime
from sqlalchemy import inspect, text

from app import db


def _ensure_schema_migrations_table():
    db.session.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                applied_at DATETIME NOT NULL
            )
            """
        )
    )
    db.session.commit()


def _is_applied(name: str) -> bool:
    result = db.session.execute(
        text("SELECT 1 FROM schema_migrations WHERE name = :name LIMIT 1"),
        {"name": name},
    ).first()
    return result is not None


def _mark_applied(name: str):
    db.session.execute(
        text(
            """
            INSERT INTO schema_migrations (name, applied_at)
            VALUES (:name, :applied_at)
            """
        ),
        {"name": name, "applied_at": datetime.utcnow().isoformat()},
    )
    db.session.commit()


def _migration_add_question_type_column():
    migration_name = "20260318_add_question_type_to_question"
    if _is_applied(migration_name):
        return

    inspector = inspect(db.engine)
    if not inspector.has_table("question"):
        _mark_applied(migration_name)
        return

    columns = {column["name"] for column in inspector.get_columns("question")}
    if "question_type" not in columns:
        db.session.execute(
            text(
                "ALTER TABLE question "
                "ADD COLUMN question_type VARCHAR(20) NOT NULL DEFAULT 'scale'"
            )
        )
        db.session.commit()
        print("Migration applied: added question.question_type")

    _mark_applied(migration_name)


def _migration_add_response_text_answer_column():
    migration_name = "20260318_add_text_answer_to_response"
    if _is_applied(migration_name):
        return

    inspector = inspect(db.engine)
    if not inspector.has_table("response"):
        _mark_applied(migration_name)
        return

    columns = {column["name"] for column in inspector.get_columns("response")}
    if "text_answer" not in columns:
        db.session.execute(
            text(
                "ALTER TABLE response "
                "ADD COLUMN text_answer TEXT NULL"
            )
        )
        db.session.commit()
        print("Migration applied: added response.text_answer")

    _mark_applied(migration_name)


def run_schema_migrations():
    """Run lightweight, idempotent SQL migrations before app startup."""
    _ensure_schema_migrations_table()
    _migration_add_question_type_column()
    _migration_add_response_text_answer_column()
