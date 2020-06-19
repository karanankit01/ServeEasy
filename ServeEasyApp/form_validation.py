from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
import re
from wtforms import validators, ValidationError

class SignupForm(FlaskForm):
   name = StringField('name',validators=[DataRequired(message="name is required")])
   email = StringField('Email',validators=[Email(message = "Enter a valid email"),DataRequired()])
   password = PasswordField('Password',validators=[DataRequired()])
   def validate_password(form,field):
      if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
,field.data):
         raise ValidationError("Enter Strong Password")
   username = StringField('username',validators=[DataRequired()])
   phone = StringField('phone',validators=[DataRequired()])
   def validate_phone(form,field):
       if not re.match(r'^[0][1-9]\d{9}$|^[1-9]\d{9}$',field.data):
          raise ValidationError("enter valid phone number")
   submit = SubmitField('Submit')