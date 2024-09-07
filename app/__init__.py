#-------CREACION DE LA APLICACION APP
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#----inicializador de objetos
bootstrap = Bootstrap()
database = SQLAlchemy()
bcrypt = Bcrypt()

#----creacion del login manager, permite saber el usaurio esta en linea o no o autenticado
login_manager = LoginManager()
login_manager.login_view = "usuario.login_usuario"
login_manager.session_protection = "strong"


#---creacion del metodo crear app
def create_app(config_type):
    app = Flask(__name__)

    #----configuracion de la aplicacion de carpeta config
    configuracion = os.path.join(os.getcwd(), "config", config_type + ".py")
    app.config.from_pyfile(configuracion)

    #----inicializacion de objetos de la app
    bootstrap.init_app(app)
    database.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)



    #----registro de blueprints
    #como se usan dos bluprints se tiene que poner un prefijo en cada una por si hay archivos del mismo nombre
    from app.user_manager import user_manager
    app.register_blueprint(user_manager, url_prefix='/user_manager')

    from app.usuario import usuario
    app.register_blueprint(usuario, url_prefix='/usuario')


    return app


