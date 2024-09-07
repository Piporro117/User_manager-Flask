#-------RUTAS DE BLUEPRINT USERIO
from flask import Flask, render_template, flash, redirect, url_for
from app.usuario import usuario
from app.usuario.forms import RegistroUsuarioFormulario, LoginUsuarioFormulario, CambioContrasenaFormulario, ActualizarPerfilFormulario
from flask_login import current_user, login_user, logout_user, login_required
from app.usuario.models import Usuario
from app import bcrypt, database #para el cambio de contraseña

#---rutas de usuario normal
@usuario.route("/")
def index():
    return render_template("index_usuario.html")


#--RUTA HOME
@usuario.route('/home')
def home():
    return render_template('home_usuario.html')


#--ruta de registro de usuario
@usuario.route('/registro', methods=['GET', 'POST'])
def registro_usuario():
    if current_user.is_authenticated:
        flash("Ya estas con una cuenta")
        return redirect(url_for('usuario.home'))
    
    form = RegistroUsuarioFormulario() 

    if form.validate_on_submit():
        Usuario.crear_usaurio(
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            rpe=form.rpe.data,
            email=form.correo.data,
            contrasena=form.contrasena.data
        )

        flash("Registro exitoso, espera a que su cuenta sea dada de alta por el administrador")

        return redirect(url_for('usuario.login_usuario'))

    context = {
        "formulario": form
    }
    return render_template('registro_usuario.html', **context) 


#--ruta de inicio de sesion de usuario
@usuario.route('/inicio_sesion', methods=["GET", 'POST'])
def login_usuario():

    #si el usuario ya esta en cuenta
    if current_user.is_authenticated:
        flash("YA ESTAS EN CUENTA")
        return redirect(url_for('usuario.home'))
    

    formulario = LoginUsuarioFormulario()

    #si el formulario fue valido
    if formulario.validate_on_submit():
        usuario = Usuario.query.filter_by(usuario_rpe= formulario.rpe.data).first()

        #checa si existe o no el usuairo
        if not usuario or not usuario.checar_contrasena(formulario.contrasena.data):
            flash("Credenciales invalidas", 'danger')
            return redirect(url_for('usuario.login_usuario'))
        
        #checa su el usuario si esta dado de alta:
        if usuario and usuario.status == 0:
            flash("TU USUARIO NO ESTA DADO DE ALTA POR FAVOR ESPERE", 'danger')
            return redirect(url_for('usuario.login_usuario'))
        
        #entrar como usuario
        login_user(usuario)
        return redirect(url_for('usuario.home'))

    context = {
        "formulario": formulario
    }

    return render_template('login_usuario.html', **context)


#--vista de dashboard
@usuario.route('/dashboard')
@login_required
def dashboard_usuario():
    if isinstance(current_user, Usuario):

        rpe_usuario = current_user.usuario_rpe
        nombre_usuario = current_user.usuario_nombres
        apellidos_usuario = current_user.usuario_apellidos
        email_usuario = current_user.usuario_email

        context = {
            'rpe':rpe_usuario,
            'nombres':nombre_usuario,
            'apellidos':apellidos_usuario,
            'email':email_usuario
        }

        return render_template('dashboard_usuario.html', **context)
    else:
        return render_template('dashboard_usuario.html')
    

#--logout de usuario
@usuario.route('/logout')
def logout_usuario():
    logout_user()
    return redirect(url_for('usuario.login_usuario'))


#--vista para cambiar contraseña del usuario
@usuario.route('/cambio_contrasena', methods=['GET', 'POST'])
@login_required
def cambio_contrasena():
    formulario = CambioContrasenaFormulario()
        
    if formulario.validate_on_submit():
        #se crea un objeto usuario para ver si existe y si es asi sacar su id y sus datos
        usuario = Usuario.query.filter_by(usuario_rpe= current_user.usuario_rpe).first()

        if usuario.checar_contrasena(formulario.contrasena_actual.data):
            #se le dice que la contrasena del usuario ahora es la nueva
            usuario.usuario_contrasena = bcrypt.generate_password_hash(formulario.contrasena_nueva.data).decode("utf-8")

            #tambien se puede de la siguiente manera pero solo es recomendable con muchos registros de actualziar:
            '''
             Usuario.query.filter_by(id=current_user.id).update({
                'usuario_contrasena': bcrypt.generate_password_hash(formulario.contrasena_nueva.data).decode("utf-8")
            })
            '''

            #se aplican los datos
            database.session.commit()

            flash("Los cambio se realizaron de manera correcta")
            redirect(url_for('usuario.dashboard_usuario'))


    context = {
            'formulario':formulario    
        }

    return render_template('cambio_contrasena.html', **context)

#--vista actualizar perfil de usuario:
@usuario.route('/actualizar_perfil', methods=['GET', 'POST'])
@login_required
def actualizar_perfil():
    #se saca informacion del usuario actual 
    usuario = current_user

    #se prellena la informacion del usuario el formulario
    formulario = ActualizarPerfilFormulario(
        nombres= usuario.usuario_nombres,
        apellidos=usuario.usuario_apellidos,
        email=usuario.usuario_email
    )


    #si es valida el post del fromulario
    if formulario.validate_on_submit():
        #se aplican los nuevos datos al usuario
        usuario.usuario_nombres = formulario.nombres.data
        usuario.usuario_apellidos = formulario.apellidos.data
        usuario.usuario_email = formulario.email.data

        #se aplica el commit()
        database.session.commit()

        flash("Tu perfil se actualizo perfectamente", 'success')
        return redirect(url_for('usuario.dashboard_usuario'))
    
    context = {
        'formulario':formulario
    }

    return render_template('actualizar_perfil.html', **context)
