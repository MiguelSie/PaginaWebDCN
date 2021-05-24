from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistroProveedor(FlaskForm):
    username = StringField('Nombre de proveedor ', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Definir token de inicio", validators=[DataRequired()])
    confirm_password = PasswordField("Rectificar Token", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrar Proveedor")

class IngresoProveedor(FlaskForm):
    password = PasswordField("Ingrese el token", validators=[DataRequired()])
    submit = SubmitField("Ingresar")