from .main import main_bp
from .admin import admin_bp


def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
