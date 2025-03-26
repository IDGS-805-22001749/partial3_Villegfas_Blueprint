from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from models import db, User
from datetime import datetime, date
from forms import GrupoForm, LoginForm, RegistroForm
import forms
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints import login_blueprint, alumnos_blueprint, profesores_blueprint
import logging


logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]')
logger = logging.getLogger(__name__)

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/", methods=['GET', 'POST'])
@login_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == "alumno":
            return redirect(url_for('index'))
        elif current_user.role == "profesor":
            return redirect(url_for('profesores.indexProfesores'))

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            logger.info(f"Usuario '{username}' inició sesión exitosamente.")

            
            if user.role == "alumno":
                return redirect(url_for('index'))
            elif user.role == "profesor":
                return redirect(url_for('profesores.indexProfesores'))
        else:
            logger.warning(f"Intento fallido de inicio de sesión para usuario '{username}'.")
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form) 


@login_blueprint.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f"Usuario '{username}' cerró sesión.")
    return redirect(url_for('login.login'))


@login_blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()  

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        role = form.role.data  
        
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            logger.warning(f"Intento de registro con nombre de usuario existente: '{username}'.")
            flash('Este nombre de usuario ya está registrado. Por favor elige otro.', 'warning')
            return render_template('registro.html', form=form)

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, role=role)
            
            db.session.add(new_user)
            db.session.commit()

            logger.info(f"Usuario registrado exitosamente: '{username}' con rol '{role}'.")
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('login.login')) 

        except Exception as e:
            logger.error(f"Error al registrar usuario '{username}': {e}")
            flash('Ocurrió un error al registrar el usuario.', 'danger')

    return render_template('registro.html', form=form)
