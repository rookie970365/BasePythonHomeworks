from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length



class CreateUserForm(FlaskForm):
    name = StringField(
        label="User name",
        name="user-name",
        validators=[
            DataRequired(),
            Length(min=3, max=100),
        ],
    )
    is_new = BooleanField(
        label="Is new user?",
        default=False,
    )
