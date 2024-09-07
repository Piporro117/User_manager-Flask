#-------INICIALIZADOR DEL BLUPRINT USER_MANAGER
from flask import Blueprint

#---creacion del blueprint indicando su nombre y carpeta templates
user_manager = Blueprint("user_manager", __name__, template_folder="templates")

#---indicar sus rutas
from app.user_manager import views