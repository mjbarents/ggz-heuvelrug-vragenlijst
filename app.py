from flask import Flask
from models import db
from config import Config
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

register_blueprints(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=app.config["PORT"])
