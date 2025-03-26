from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Alumnos, Preguntas, Respuestas, User, Profesores
from datetime import datetime, date
from forms import GrupoForm, LoginForm, RegistroForm
import forms
from flask_login import LoginManager, login_user, login_required, logout_user,  current_user 
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints import profesores_blueprint
import logging
from functools import wraps


logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]')
logger = logging.getLogger(__name__)


def profesor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'profesor':
            return f(*args, **kwargs)
        else:
            flash("No tienes permisos para acceder a esta página.", "danger")
            return redirect(url_for('index')) 
    return decorated_function

profesores_blueprint = Blueprint('profesores', __name__)

@profesores_blueprint.route('/indexProfesores')
@login_required
@profesor_required
def indexProfesores():
    return render_template('indexProfesores.html')


@profesores_blueprint.route('/profesores', methods=['GET', 'POST'])
@login_required
@profesor_required
def profesores():
    create_form = forms.FormProfesores(request.form)
    profesores=Profesores.query.all()   

    return render_template('profesores.html', form=create_form,profesores=profesores)

@profesores_blueprint.route('/preguntas', methods=['GET','POST'])
@login_required
@profesor_required
def preguntas():
    create_form = forms.FormPreguntas(request.form)
    
    if request.method == 'POST':
        pre = Preguntas(
            materia=create_form.materia.data,
            pregunta=create_form.pregunta.data,
            a=create_form.a.data,
            b=create_form.b.data,
            c=create_form.c.data,
            d=create_form.d.data,
            respuestaCorrecta=create_form.respuestaCorrecta.data
        )
        db.session.add(pre)
        db.session.commit()
        
        logger.info(f"Pregunta agregada por el usuario '{current_user.username}': {pre.pregunta} ({pre.materia})")
        flash("Pregunta agregada exitosamente.")
        return redirect(url_for('index'))

    return render_template('preguntas.html', form=create_form)

@profesores_blueprint.route('/calificaciones', methods=['GET', 'POST'])
@login_required
@profesor_required
def calificaciones():
    create_form = GrupoForm(request.form)
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    create_form.grupo.choices = [(grupo[0], grupo[0]) for grupo in grupos]

    alumnos = []
    grupo_seleccionado = None

    if request.method == 'POST' and create_form.validate_on_submit():
        grupo_seleccionado = create_form.grupo.data
        alumnos = db.session.query(Respuestas).filter_by(grupo=grupo_seleccionado).all()
        
        logger.info(f"Usuario '{current_user.username}' visualizó las calificaciones del grupo '{grupo_seleccionado}'.")
        
    return render_template('calificaciones.html', form=create_form, alumnos=alumnos, grupo_seleccionado=grupo_seleccionado)


@profesores_blueprint.route('/agregar', methods=['GET', 'POST'])
@login_required
@profesor_required  
def agregar():
    create_form=forms.FormProfesores(request.form)
    if request.method == 'POST':
        prof=Profesores(nombre=create_form.nombre.data,
                     apaterno=create_form.apaterno.data,
                     email=create_form.email.data)
        #insert alumnos() values()

        db.session.add(prof)
        db.session.commit()
        return redirect(url_for('profesores.indexProfesores'))
    return render_template('agregar.html', form = create_form)


@profesores_blueprint.route('/modificar', methods=['GET', 'POST'])
@login_required
@profesor_required
def modificar():
    create_form= forms.FormProfesores(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        # select * from profesores where id == id
        prof1 = db.session.query(Profesores).filter(Profesores.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=str.rstrip(prof1.nombre)
        create_form.apaterno.data=prof1.apaterno
        create_form.email.data=prof1.email
    if request.method=='POST':
        id=create_form.id.data
        prof1 = db.session.query(Profesores).filter(Profesores.id==id).first()
        prof1.id = id
        prof1.nombre=str.rstrip(create_form.nombre.data)
        prof1.apaterno=create_form.apaterno.data
        prof1.email=create_form.email.data
        db.session.add(prof1)
        db.session.commit()
        return redirect(url_for('profesores.indexProfesores'))
    return render_template('modificar.html', form=create_form)


@profesores_blueprint.route('/detalles', methods=['GET', 'POST'])
@login_required
@profesor_required
def detalles():
    create_form=forms.FormProfesores(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        prof1=db.session.query(Profesores).filter(Profesores.id==id).first()
        nombre=prof1.nombre
        apaterno=prof1.apaterno
        email=prof1.email
    return render_template("detalles.html",form=create_form,nombre=nombre,apaterno=apaterno,email=email)


@profesores_blueprint.route('/eliminar', methods=['GET', 'POST'])
@login_required
@profesor_required  
def eliminar():
    create_form = forms.FormProfesores(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        #Select from profesores where id = id
        prof1 = db.session.query(Profesores).filter(Profesores.id == id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=prof1.nombre
        create_form.apaterno.data=prof1.apaterno
        create_form.email.data=prof1.email
    if request.method == 'POST':
        id=create_form.id.data
        prof = Profesores.query.get(id)
        db.session.delete(prof)
        db.session.commit()
        return redirect(url_for('profesores.indexProfesores'))
    return render_template("eliminar.html", form=create_form)