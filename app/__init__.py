"""Flask application factory."""

from flask import Flask, request, session
from flask_babel import Babel

from app.config import Config
from app.db import close_db_connection
from app.routes.customer import bp as customer_bp
from app.routes.index import bp as index_bp
from app.routes.invoice import bp as invoice_bp
from app.routes.product import bp as product_bp
from app.routes.search import bp as search_bp


def get_locale() -> str:
    """Resolve the active locale from session or browser preferences."""
    selected_locale = session.get("lang")
    if selected_locale in {"el", "en"}:
        return selected_locale
    browser_locale = request.accept_languages.best_match(["el", "en"])
    return browser_locale or "el"


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    babel = Babel()
    babel.init_app(app, locale_selector=get_locale)

    @app.context_processor
    def inject_locale() -> dict[str, str]:
        """Expose current locale to templates."""
        return {"current_locale": get_locale()}

    app.teardown_appcontext(close_db_connection)

    app.register_blueprint(index_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(search_bp)

    return app
