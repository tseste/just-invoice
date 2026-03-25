"""Application entry point."""

import os

from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.environ.get("APP_HOST", "0.0.0.0"),
        port=int(os.environ.get("APP_PORT", "5000")),
        debug=app.config["FLASK_DEBUG"],
    )
