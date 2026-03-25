"""Required Forms."""

from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms.fields import (
    DecimalField,
    EmailField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Length


class CustomerForm(FlaskForm):
    """The form for customer insert or update."""

    FirstName = StringField(label=_l("Όνομα"), validators=[InputRequired()])
    LastName = StringField(label=_l("Επώνυμο"), validators=[InputRequired()])
    Company = StringField(label=_l("Επάγγελμα"))
    Address = StringField(label=_l("Διεύθυνση"))
    City = StringField(label=_l("Πόλη"))
    Country = StringField(label=_l("Χώρα"))
    PostalCode = StringField(label=_l("Ταχυδρομικός Κώδικας"))
    Phone = StringField(label=_l("Τηλέφωνο"))
    Fax = StringField()
    Email = EmailField()
    TRN = StringField(
        label=_l("Α.Φ.Μ."),
        validators=[
            InputRequired(),
            Length(min=9, max=9, message=_l("Το Α.Φ.Μ. έχει 9 ψηφία.")),
        ],
    )
    TaxOffice = StringField(label=_l("Δ.Ο.Υ."))


class CustomDecimalField(DecimalField):
    """Custom decimal field."""

    def process_formdata(self, valuelist):
        """Allow both dot and comma as decimal seperators."""
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super().process_formdata(valuelist)


class ProductForm(FlaskForm):
    """The form for product insert or update."""

    Name = StringField(label=_l("Όνομα Προϊόντος"), validators=[InputRequired()])
    Description = TextAreaField(label=_l("Περιγραφή"))
    UnitTypeId = SelectField(label=_l("Μονάδα Μέτρησης"), validators=[InputRequired()])
    UnitPrice = CustomDecimalField(
        label=_l("Τιμή"), places=2, validators=[InputRequired()]
    )
