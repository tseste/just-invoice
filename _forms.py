"""Required Forms."""
from flask_wtf import FlaskForm
from wtforms.fields import (StringField, DecimalField, TextAreaField,
                            SelectField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length


class CustomerForm(FlaskForm):
    """The form for customer insert or update."""

    FirstName = StringField(label='Όνομα', validators=[InputRequired()])
    LastName = StringField(label='Επώνυμο', validators=[InputRequired()])
    Company = StringField(label='Επάγγελμα')
    Address = StringField(label='Διεύθυνση')
    City = StringField(label='Πόλη')
    Country = StringField(label='Χώρα')
    PostalCode = StringField(label='Ταχυδρομικός Κώδικας')
    Phone = StringField(label='Τηλέφωνο')
    Fax = StringField()
    Email = EmailField()
    TRN = StringField(label='Α.Φ.Μ.',
                      validators=[InputRequired(),
                                  Length(min=9, max=9,
                                         message='Το Α.Φ.Μ. έχει 9 ψηφία.')])
    TaxOffice = StringField(label='Δ.Ο.Υ.')


class CustomDecimalField(DecimalField):
    """Custom decimal field."""

    def process_formdata(self, valuelist):
        """Allow both dot and comma as decimal seperators."""
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(CustomDecimalField, self).process_formdata(valuelist)


class ProductForm(FlaskForm):
    """The form for product insert or update."""

    Name = StringField(label='Όνομα Προϊόντος', validators=[InputRequired()])
    Description = TextAreaField(label='Περιγραφή')
    UnitTypeId = SelectField(label='Μονάδα Μέτρησης',
                             validators=[InputRequired()])
    UnitPrice = CustomDecimalField(label='Τιμή', places=2,
                                   validators=[InputRequired()])
