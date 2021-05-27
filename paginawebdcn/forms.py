from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from paginawebdcn.ModelosDB import Proveedor


class RegistroProveedor(FlaskForm):
    name = StringField('Nombre de proveedor ', validators=[DataRequired(), Length(min=2, max=80)])
    username = StringField('Nombre de usuario ', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Definir token de inicio", validators=[DataRequired()])
    confirm_password = PasswordField("Rectificar Token", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrar Proveedor")

    def validate_name(self, name):
        proveedor = Proveedor.query.filter_by(name=name.data).first()
        if proveedor:
            raise ValidationError('El nombre ingresado ya se encuentra registrado')

    def validate_username(self, username):
        proveedor = Proveedor.query.filter_by(username=username.data).first()
        if proveedor:
            raise ValidationError('El usuario ingresado ya se encuentra registrado')

    def validate_email(self, email):
        proveedor = Proveedor.query.filter_by(email=email.data).first()
        if proveedor:
            raise ValidationError('El correo electronico  ingresado ya se encuentra registrado')


class IngresoProveedor(FlaskForm):
    username = StringField('Ingrese el nombre de usuario ', validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField("Ingrese el token", validators=[DataRequired()])
    submit = SubmitField("Ingresar")


class IngresoAdministrador(FlaskForm):
    email = StringField("Ingrese el correo", validators=[DataRequired(), Email()])
    password = PasswordField("Ingrese la contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")
