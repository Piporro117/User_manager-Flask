#---FORMULARIOS PARA LA BLUEPRINT ADMIN
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
#from app.user_manager import models


#---formulario para inicio de sesion con Amdin
class LoginAdminFormulario(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired()])
    contrasena = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Entrar")

#---FORMULARIO PARA CAMBIO SE CONTRASEÑA
class CambiarContraseñaAdminForm(FlaskForm):
    contrasena_actual = PasswordField("Contraseña Actual", validators=[DataRequired()])
    contrasena_nueva = PasswordField("Nueva Contraseña", validators=[DataRequired()])
    contrasena_confirmacion = PasswordField("Confirme Nueva Contraseña", validators=[DataRequired()])
    submit = SubmitField("Cambiar contraseña")

#---BARRA DE BUSQUEDA DE USUARIOS
class BarraBusquedaUsuarios(FlaskForm):
    usuario_buscar = StringField(validators=[DataRequired()])
    submit = SubmitField("Buscar")

