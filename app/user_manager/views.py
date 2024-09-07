#-------RUTAS DE BLUEPRINT USER_MANAGER
from flask import Flask, render_template, flash, redirect, url_for
from app.user_manager import user_manager
from app.user_manager.forms import LoginAdminFormulario, CambiarContraseñaAdminForm, BarraBusquedaUsuarios
from flask_login import current_user, login_user, login_required, logout_user
from app.usuario.models import Usuario
from app import database, bcrypt


#metodo para saber si eres admin o no
def es_admin(usuario):
    if usuario.rol != "Admin":
        return False
    else:
        return True

#---rutas de user_manager
@user_manager.route("/", methods=['GET', 'POST'])
def index():

    formulario = LoginAdminFormulario()

    
    #si ya estas en admin
    if current_user.is_authenticated:
        flash("YA ESTAS EN CUENTA")
        return redirect(url_for('usuario.home'))
    

    #si el formulario fue valido 
    if formulario.validate_on_submit():

        admi = Usuario.query.filter_by(rol="Admin").first()

        if admi and admi.checar_contrasena(formulario.contrasena.data):
            login_user(admi)
            flash("Incio de sesion admin exitoso", 'success')
            return redirect(url_for('user_manager.dashboard_admin'))
    
        else:
            flash("Credenciales incorrectas intente de nuevo", 'danger')
            return redirect(url_for('user_manager.index'))
    

    context = {
        'formulario':formulario
    }
    

    return render_template("index_admin.html", **context)


#---vista dashboard admin
@user_manager.route('/dashboard')
@login_required
def dashboard_admin():

    if es_admin(current_user) == False:
        redirect(url_for("user_manager.index"))

    admin = current_user

    #sacar informacion de la base de datos

    #total de una tabla
    total_usuarios = Usuario.query.count()

    #total de usuarios no aprobados
    usuarios_no_aprobados = Usuario.query.filter_by(status=0).count()

    #totoal de usuarios aprobados
    usuarios_aprobados = Usuario.query.filter_by(status=1).count()

    context = {
        'nombre':admin.usuario_nombres,
        'total_usuarios':total_usuarios,
        'usuarios_no_aprobados':usuarios_no_aprobados,
        'usuarios_aprobados':usuarios_aprobados
    }

    return render_template('dashboard_admin.html', **context)


#---vista logout
@user_manager.route('/logout')
def logout_admin():
    logout_user()
    return redirect(url_for('user_manager.index'))



#---vista para ver todos los usuarios
@user_manager.route('/ver_usuarios', methods=['POST', 'GET'])
@login_required
def ver_usuarios():

    if es_admin(current_user) == False:
        return redirect(url_for('user_manager.index'))

    
    barra = BarraBusquedaUsuarios()

    #validacion para saber si se uso o no los usuarios
    if barra.validate_on_submit():
        usuario_buscar = barra.usuario_buscar.data
        usuarios = Usuario.query.filter(Usuario.usuario_nombres.like(f"%{usuario_buscar}%")).all()
        context={'usuarios':usuarios,
                 'barra':barra}
        return render_template("ver_usuario.html", **context)


    #sacamos todos los usuarios en forma de lista
    usuarios = Usuario.query.all()

    context = {
        'usuarios':usuarios,
        'barra':barra
    }


    return render_template("ver_usuario.html", **context)


#---vista para aprobar usuarios, se le pasa el id en la url
@user_manager.route('/aprobar_usuario/<int:id>')
@login_required
def aprobar_usuario(id):

    #se filtra el usuario
    usuario_actualizar = Usuario.query.filter_by(id=id).first()

    #si existe el usuario
    if usuario_actualizar:
        # se cambia su atributo status de 0 a 1
        usuario_actualizar.status = 1

        flash(f"El usuario con el id:{id} se ha aprovado con exito")
    
        #se aplica los cambios a la base de datos
        database.session.commit()


    return redirect(url_for('user_manager.ver_usuarios'))

#---vista para cambiar contraseña usuairo
@user_manager.route('/cambiar_contrasena_admin', methods=['POST', 'GET'])
@login_required
def cambiar_contrasena_admin():

    #checa si es admin
    if es_admin(current_user) == False:
        return redirect(url_for('usuario.login_usaurio'))
    
    formulario = CambiarContraseñaAdminForm()


    if formulario.validate_on_submit():
        admin = Usuario.query.filter_by(rol='Admin', id=current_user.id).first()

        if admin and admin.checar_contrasena(formulario.contrasena_actual.data):
            admin.usuario_contrasena = bcrypt.generate_password_hash(formulario.contrasena_nueva.data).decode('utf-8')
            database.session.commit()

            flash("Se cambio la contraseña correctamente", 'success')
            return redirect(url_for('user_manager.dashboard_admin'))

        else:
            flash("Contraseña actual no correcta", 'danger')
            return redirect(url_for('user_manager.cambiar_contrasena_admin'))


    context = {
        'formulario':formulario
    }

    return render_template("cambio_contrasena_admin.html", **context)




