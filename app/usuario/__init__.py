#-------INICIALIZADOR DEL BLUPRINT USER_MANAGER
from flask import Blueprint

#---creacion del blueprint indicando su nombre y carpeta templates
usuario = Blueprint("usuario", __name__, template_folder="templates")

#---indicar sus rutas
from app.usuario import views