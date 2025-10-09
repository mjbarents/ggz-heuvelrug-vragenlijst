from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
)
from models import db, Question, Token, Response
from functools import wraps
from sqlalchemy import func

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            if request.endpoint != "admin.admin_dashboard":
                flash(
                    "Log alstublieft in om toegang te krijgen tot het admin panel.",
                    "warning",
                )
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == current_app.config["ADMIN_USERNAME"]
            and password == current_app.config["ADMIN_PASSWORD"]
        ):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Ongeldige inloggegevens.", "error")

    return render_template("admin_login.html")


@admin_bp.route("/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.admin_login"))


@admin_bp.route("/")
@admin_required
def admin_dashboard():
    total_tokens = Token.query.count()
    used_tokens = Token.query.filter_by(used=True).count()
    total_responses = Response.query.count()
    total_questions = Question.query.count()

    responses = (
        db.session.query(
            Response.id,
            Response.token_id,
            Response.submitted_at,
            Question.text,
            Response.score,
        )
        .join(Question)
        .order_by(Response.token_id, Question.order)
        .all()
    )

    grouped_responses = {}
    for response in responses:
        token_id = response.token_id
        if token_id not in grouped_responses:
            grouped_responses[token_id] = {
                "token_id": token_id,
                "submitted_at": response.submitted_at,
                "answers": [],
            }
        grouped_responses[token_id]["answers"].append(
            {"question": response.text, "score": response.score}
        )

    questions = Question.query.order_by(Question.order).all()
    stats = []
    for question in questions:
        scores = [
            r.score for r in Response.query.filter_by(question_id=question.id).all()
        ]
        if scores:
            avg_score = sum(scores) / len(scores)
            stats.append(
                {
                    "question": question.text,
                    "avg_score": round(avg_score, 1),
                    "responses": len(scores),
                    "scores": scores,
                }
            )

    return render_template(
        "admin_dashboard.html",
        total_tokens=total_tokens,
        used_tokens=used_tokens,
        total_responses=total_responses,
        total_questions=total_questions,
        grouped_responses=grouped_responses.values(),
        stats=stats,
    )


@admin_bp.route("/questions")
@admin_required
def admin_questions():
    questions = Question.query.order_by(Question.order).all()
    return render_template("admin_questions.html", questions=questions)


@admin_bp.route("/questions/add", methods=["POST"])
@admin_required
def admin_add_question():
    text = request.form.get("text")
    if text:
        max_order = db.session.query(func.max(Question.order)).scalar() or 0
        question = Question(text=text, order=max_order + 1)
        db.session.add(question)
        db.session.commit()
        flash("Vraag succesvol toegevoegd!", "success")
    return redirect(url_for("admin.admin_questions"))


@admin_bp.route("/questions/edit/<int:id>", methods=["POST"])
@admin_required
def admin_edit_question(id):
    question = Question.query.get_or_404(id)
    text = request.form.get("text")
    if text:
        question.text = text
        db.session.commit()
        flash("Vraag succesvol bijgewerkt!", "success")
    return redirect(url_for("admin.admin_questions"))


@admin_bp.route("/questions/delete/<int:id>", methods=["POST"])
@admin_required
def admin_delete_question(id):
    question = Question.query.get_or_404(id)
    if question.responses:
        flash(
            "Deze vraag kan niet verwijderd worden omdat er al antwoorden op gegeven zijn.",
            "error",
        )
    else:
        db.session.delete(question)
        db.session.commit()
        flash("Vraag succesvol verwijderd!", "success")
    return redirect(url_for("admin.admin_questions"))


@admin_bp.route("/tokens")
@admin_required
def admin_tokens():
    tokens = Token.query.order_by(Token.created_at.desc()).all()
    return render_template("admin_tokens.html", tokens=tokens)


@admin_bp.route("/tokens/generate", methods=["POST"])
@admin_required
def admin_generate_token():
    tokens = []
    token = Token(token=Token.generate_token())
    db.session.add(token)
    tokens.append(token)
    db.session.commit()
    return redirect(url_for("admin.admin_tokens"))


@admin_bp.route("/tokens/delete/<int:id>", methods=["POST"])
@admin_required
def admin_delete_token(id):
    token = Token.query.get_or_404(id)

    if token.used and token.responses:
        flash(
            "Deze uitnodiging kan niet verwijderd worden omdat de vragenlijst al is ingevuld. "
            "Verwijder eerst de bijbehorende antwoorden als u deze uitnodiging wilt verwijderen.",
            "error",
        )
    else:
        db.session.delete(token)
        db.session.commit()
    return redirect(url_for("admin.admin_tokens"))


@admin_bp.route("/responses")
@admin_required
def admin_responses():
    return redirect(url_for("admin.admin_dashboard"))
