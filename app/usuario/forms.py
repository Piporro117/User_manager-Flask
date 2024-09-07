#-------------FORMULARIOS PARA EL BLUPRINT USUARIO
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.usuario.models import Usuario

#---metodos para validacion de email y rpe
def email_existente(form, campo):
    email = Usuario.query.filter_by(usuario_email=campo.data).first()
    if email:
        raise ValidationError("Este email ya esta registrado")
    
def rpe_existente(form, campo):
    rpe = Usuario.query.filter_by(usuario_rpe=campo.data).first()
    if rpe:
        raise ValidationError("Este rpe ya esta registrado con otro usuario")
    


#---FORMULARIO DE REGISTRO DE USUARIO
class RegistroUsuarioFormulario(FlaskForm):
    nombres = StringField("Nombres", validators=[DataRequired(), Length(4, 30, message="Nombre muy largo o muy corto")])
    apellidos = StringField("Apellidos", validators=[DataRequired(), Length(4, 30, message="Apellido muy largo o muy corto")])
    rpe = StringField("R.P.E", validators=[DataRequired(), Length(5,5, message="tamaño incorrecto"), rpe_existente])
    correo = StringField("Email", validators=[DataRequired(), Email(), email_existente])
    contrasena = PasswordField("Contraseña", validators=[DataRequired(), EqualTo("confirmacion", message="La contraseñas deben coincidir"), Length(5, 10, message="Debe tener longitud de entre 5 a 10")])
    confirmacion = PasswordField("Contraseña", validators=[DataRequired(), EqualTo("contrasena", message="La contraseñas deben coincidir"), Length(5, 10, message="Debe tener longitud de entre 5 a 10")])
    submit = SubmitField("Registrarse")


#---FORMULARIO DE LOGIN USUARIO
class LoginUsuarioFormulario(FlaskForm):
    rpe = StringField("R.P.E", validators=[DataRequired()])
    contrasena = PasswordField("Contraseña", validators=[DataRequired(), Length(5,10, message="Tamaño invalido")])
    submit = SubmitField("Entrar")

    
#---FORMULARIO PARA CAMBIAR CONTRASEÑA
class CambioContrasenaFormulario(FlaskForm):
    contrasena_actual = PasswordField("Contraseña actual", validators=[DataRequired(), Length(5,10, message="Tamaño invalido")])
    contrasena_nueva = PasswordField("Contraseña nueva", validators=[DataRequired(), Length(5,10, message="Tamaño invalido")])
    contrasena_confirmacion = PasswordField("Confirme contraseña nueva", validators=[DataRequired(),Length(5,10, message="Tamaño invalido"), EqualTo("contrasena_nueva", message="Deben coincidir las contraseñas")])
    submit = SubmitField("Cambiar contraseña")


#---FROMULARIO DE ACTUALIZACION DE PERFIL
class ActualizarPerfilFormulario(FlaskForm):
    nombres = StringField("Nombre(s):", validators=[DataRequired(), Length(4, 30, message="Nombre invalido")])
    apellidos = StringField("Apellidos:", validators=[DataRequired(), Length(4,30 , message="Apellidos no validos")])
    email = StringField("Email", validators=[Email(), DataRequired()])
    submit = SubmitField("Actualizar")