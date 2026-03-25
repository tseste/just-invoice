"""Database and filesystem helpers."""

from pathlib import Path

import pymysql
from flask import current_app, g


def get_db_connection():
    """Get request-scoped MySQL connection."""
    if "mysql_conn" not in g:
        g.mysql_conn = pymysql.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            passwd=current_app.config["DB_PASSWORD"],
            port=current_app.config["DB_PORT"],
            db=current_app.config["DB_NAME"],
            use_unicode=True,
            charset="utf8",
        )
    return g.mysql_conn


def close_db_connection(_error):
    """Close request-scoped MySQL connection at request end."""
    connection = g.pop("mysql_conn", None)
    if connection is not None:
        connection.close()


def get_pdf_output_dir() -> Path:
    """Return configurable PDF output directory."""
    return Path(current_app.config["PDF_OUTPUT_DIR"])
