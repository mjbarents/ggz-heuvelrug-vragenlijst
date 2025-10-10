from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models import db
from config import Config
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
db.init_app(app)

register_blueprints(app)


# Basic security headers
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=app.config["PORT"])
