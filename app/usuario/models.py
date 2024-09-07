#---CREACION DE TABLAS DE USUARIOS
from app import database, bcrypt
from app import login_manager
from flask_login import UserMixin

from datetime import datetime


#Tabla usuarios, esta sera creada con roles
class Usuario(UserMixin, database.Model):
    __tablename__ = "usuarios"

    #creacion de los atributos
    id = database.Column(database.Integer, primary_key=True)
    usuario_nombres = database.Column(database.String(40))
    usuario_apellidos = database.Column(database.String(40))
    usuario_rpe = database.Column(database.String(5), unique=True, index= True)
    usuario_email = database.Column(database.String(40), unique=True)
    usuario_contrasena = database.Column(database.String(25))
    usuario_creacion = database.Column(database.DateTime, default=datetime.now)
    status = database.Column(database.Integer, default=0)
    rol = database.Column(database.String(20), default="normal")

    #--funciones para v alidacion de contraseña
    def checar_contrasena(self, contrasena):
        return bcrypt.check_password_hash(self.usuario_contrasena, contrasena)
    

    #--metodo para la creacion de un usuario
    @classmethod
    def crear_usaurio(cls,nombres, apellidos, rpe, email, contrasena, rol="normal"):
        usuario = cls(usuario_nombres=nombres,
                      usuario_apellidos=apellidos,
                      usuario_rpe=rpe,
                      usuario_email= email,
                      usuario_contrasena= bcrypt.generate_password_hash(contrasena).decode("utf-8"),
                      rol=rol
                      )
        
        #agregar el usuario a la base de datos
        database.session.add(usuario)
        database.session.commit()
        return usuario
    

#metodo para permitir la carga de usuario y saber si esta con sesion o no
@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))