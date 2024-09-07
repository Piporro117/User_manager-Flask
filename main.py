#-------------archivo principal
from app import create_app, database
from app.usuario.models import Usuario


aplicacion  = create_app("developer")


#para la aplicacion de base de datos y creacion de tablas
with aplicacion.app_context():

    #creacionde tablas
    database.create_all() 

    #creacion del administrador si no existe
    admin_existe = Usuario.query.filter_by(rol="Admin").first()

    if admin_existe is None:
        admin = Usuario.crear_usaurio(
            nombres="admin",
            apellidos="Administrador",
            rpe="GR968",
            email="mauriciern@gmail.com",
            contrasena="admin",
            rol="Admin"
        )

        admin.status = 1

        database.session.add(admin)
        database.session.commit()


    aplicacion.run()


