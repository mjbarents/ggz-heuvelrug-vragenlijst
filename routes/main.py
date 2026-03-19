from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Question, Token, Response
from datetime import datetime, timezone

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/survey/<token_string>")
def survey(token_string):
    token = Token.query.filter_by(token=token_string).first()

    if not token:
        flash("Ongeldige uitnodigingslink. Controleer alstublieft uw link.", "error")
        return render_template(
            "error.html",
            message="Ongeldige uitnodigingslink. Deze link bestaat niet of is verlopen.",
        )

    if token.used:
        flash("Deze vragenlijst is al ingevuld.", "warning")
        return render_template(
            "error.html",
            message="Deze vragenlijst is al ingevuld. Elke uitnodiging kan maar één keer gebruikt worden.",
        )

    questions = Question.query.order_by(Question.order).all()
    return render_template("survey.html", questions=questions, token=token_string)


@main_bp.route("/submit_survey", methods=["POST"])
def submit_survey():
    token_string = request.form.get("token")
    token = Token.query.filter_by(token=token_string).first()

    if not token or token.used:
        flash("Ongeldige of reeds gebruikte uitnodiging.", "error")
        return redirect(url_for("main.index"))

    questions = Question.query.all()

    for question in questions:
        if question.question_type == "scale":
            score = request.form.get(f"question_{question.id}")
            if score is None or score == "":
                flash(
                    "Let op: U moet alle schaalvragen beantwoorden voordat u de vragenlijst kunt versturen.",
                    "warning",
                )
                return redirect(url_for("main.survey", token_string=token_string))

            try:
                score = int(score)
                if score < 0 or score > 10:
                    flash("Scores moeten tussen 0 en 10 liggen.", "error")
                    return redirect(url_for("main.survey", token_string=token_string))
            except ValueError:
                flash("Ongeldige score ingevoerd.", "error")
                return redirect(url_for("main.survey", token_string=token_string))

    for question in questions:
        if question.question_type == "open":
            text_answer = request.form.get(f"question_{question.id}", "").strip()
            response = Response(
                token_id=token.id,
                question_id=question.id,
                score=0,
                text_answer=text_answer if text_answer else None,
            )
        else:
            score = int(request.form.get(f"question_{question.id}"))
            response = Response(token_id=token.id, question_id=question.id, score=score)
        db.session.add(response)

    token.used = True
    token.used_at = datetime.now(timezone.utc)
    db.session.commit()

    return render_template("thank_you.html")
