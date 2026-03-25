"""Product routes."""

import pymysql
from flask import Blueprint, flash, json, redirect, render_template, request, url_for

from app.db import get_db_connection
from app.forms import ProductForm

bp = Blueprint("product", __name__)


@bp.route("/product", methods=["GET", "POST"])
def product():
    """Create or update a product."""
    form = ProductForm()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """SELECT UnitTypeId, Name
           FROM ProductUnitType"""
    )
    form.UnitTypeId.choices = [(str(row[0]), row[1]) for row in cursor.fetchall()]
    if form.validate_on_submit():
        form.UnitTypeId.data = int(form.UnitTypeId.data)
        cursor.callproc(
            "sp_Product",
            (
                form.Name.data,
                form.Description.data,
                form.UnitTypeId.data,
                form.UnitPrice.data,
            ),
        )
        connection.commit()
        flash("Success!")
        return redirect(url_for("product.product"))
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}")
    return render_template("product.html", form=form)


@bp.route("/product_list", methods=["POST"])
def product_list():
    """Fetch all products SQL query."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM Product")
    data = cursor.fetchall()
    names = [item[0] for item in data]
    return json.jsonify({"message": names})


@bp.route("/select_product", methods=["POST"])
def select_product():
    """Select products by name."""
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Handle both JSON and form data
    if request.is_json:
        product_name = request.json.get("ProductId")
    else:
        product_name = request.form.get("ProductId")

    if not product_name:
        return json.jsonify({})

    cursor.execute(
        """SELECT p.*, put.Name AS UnitTypeName
                FROM Product p
                INNER JOIN ProductUnitType put ON p.UnitTypeId = put.UnitTypeId
                WHERE p.Name=%s""",
        (product_name,),
    )
    data = cursor.fetchone()
    if data:
        data["UnitPrice"] = "{0:f}".format(data["UnitPrice"])
        return json.jsonify(data)
    return json.jsonify({})


@bp.route("/product_types_list", methods=["POST"])
def product_types_list():
    """Fetch all product types SQL query."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT UnitTypeId, Name FROM ProductUnitType")
    data = cursor.fetchall()
    return json.jsonify({"message": data})


@bp.route("/unittype", methods=["GET"])
def unittype():
    """Create a new product unit type."""
    return render_template("unittype.html")


@bp.route("/new_unittype", methods=["POST"])
def new_unittype():
    """Add new unit type."""
    connection = get_db_connection()
    cursor = connection.cursor()
    unit_name = request.form["Name"]
    cursor.execute(
        """SELECT Name
           FROM ProductUnitType
           WHERE Name LIKE %s""",
        (unit_name,),
    )
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute(
            """INSERT INTO ProductUnitType (Name)
               VALUES (%s)""",
            (unit_name,),
        )
        connection.commit()
    return redirect(url_for("product.unittype"))
