"""Invoice routes."""

import os

import pdfkit
from flask import (
    Blueprint,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from app.db import get_pdf_output_dir

bp = Blueprint("invoice", __name__)


@bp.route("/invoice", methods=["GET"])
def invoice():
    """Create invoice page."""

    class CompanyInfo:
        """Temporary hardcoded company data."""

        name = ""
        logo = url_for("static", filename="images/logo.png")
        job = ""
        TRN = ""
        TaxOffice = ""
        address = ""
        city = ""
        postal_code = ""
        country = ""
        phone = []
        fax = []
        email = ""
        website = ""

    company = CompanyInfo()
    return render_template("invoice.html", company=company)


@bp.route("/invoice/create_pdf", methods=["POST"])
def invoice_pdf():
    """Create invoice PDF."""

    class CompanyInfo:
        """Temporary hardcoded company data."""

        name = ""
        logo = (
            "file://"
            + os.path.abspath(".")
            + url_for("static", filename="images/logo_pdf.svg")
        )
        job = ""
        TRN = ""
        TaxOffice = ""
        address = ""
        city = ""
        postal_code = ""
        country = ""
        phone = []
        fax = []
        email = ""
        website = ""

    company = CompanyInfo()
    params = request.json
    pdf_output_dir = get_pdf_output_dir()
    pdf_output_dir.mkdir(parents=True, exist_ok=True)
    project_root = os.path.abspath(".")
    css_files = [
        os.path.join(project_root, "static", "css", "base.css"),
        os.path.join(project_root, "static", "css", "invoice.css"),
    ]
    pdf_options = {
        "enable-local-file-access": "",
        "background": "",
        "load-error-handling": "ignore",
        "load-media-error-handling": "ignore",
    }

    pdfkit.from_string(
        input=render_template("print_invoice.html", company=company, **params),
        output_path=str(pdf_output_dir / (params["InvoiceId"] + ".pdf")),
        css=css_files,
        options=pdf_options,
    )
    return redirect(url_for("invoice.view_pdf", invoice_id=params["InvoiceId"]))


@bp.route("/invoice/<invoice_id>.pdf", methods=["GET"])
def view_pdf(invoice_id: str):
    """Show pdf with the given invoice_id."""
    pdf_file = get_pdf_output_dir() / (invoice_id + ".pdf")
    if not pdf_file.exists():
        abort(404)
    with open(pdf_file, "rb") as pdf:
        response = make_response(pdf.read())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"inline; filename={invoice_id}.pdf"
    return response
