from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Alumnos, Preguntas, Respuestas, User
from datetime import datetime, date
from forms import GrupoForm, LoginForm, RegistroForm
import forms
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints import alumnos_blueprint
from functools import wraps


alumnos_blueprint = Blueprint('alumnos', __name__)

def alumno_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'alumno':
            return f(*args, **kwargs)
        else:
            flash("No tienes permisos para acceder a esta página.", "danger")
            return redirect(url_for('profesores.indexProfesores'))  
    return decorated_function


@alumnos_blueprint.route('/alumnos', methods=['GET', 'POST'])
@login_required
@alumno_required
def alumnos():
    create_form = forms.FormsAlumno(request.form)
    if request.method == 'POST':
        fechaNac = date(create_form.anio.data, create_form.mes.data, create_form.dia.data)
        hoy = date.today()
        edad = hoy.year - fechaNac.year - ((hoy.month, hoy.day) < (fechaNac.month, fechaNac.day))

        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            amaterno=create_form.amaterno.data,
            fechaNacimiento=fechaNac,
            edad=edad,
            grupo=create_form.grupo.data
        )

        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('alumnos.html', form=create_form)




@alumnos_blueprint.route('/examen', methods=['GET', 'POST'])
@login_required
@alumno_required
def examen():
    create_form = forms.FormPreguntas()

    if request.method == 'POST':
        if 'btn1' in request.form:
            nombre = request.form['nombre']
            apaterno = request.form['apaterno']
            alumno = Alumnos.query.filter_by(nombre=nombre, apaterno=apaterno).first()

            if alumno:
                preguntas = Preguntas.query.all()
                return render_template('examen.html', alumno=alumno, preguntas=preguntas, form=create_form)
            else:
                flash('Alumno no encontrado.')

        elif 'btnEnviar' in request.form:
            nombre = request.form['nombre']
            apaterno = request.form['apaterno']
            alumno = Alumnos.query.filter_by(nombre=nombre, apaterno=apaterno).first()

            if not alumno:
                flash('No se encontró al alumno.')
                return redirect('/examen')

            preguntas = Preguntas.query.all()
            total_preguntas = len(preguntas)
            respuestas_correctas = 0

            for pregunta in preguntas:
                respuesta_seleccionada = request.form.get(f'respuesta_{pregunta.id}')
                if respuesta_seleccionada == pregunta.respuestaCorrecta:
                    respuestas_correctas += 1

            calificacion = (respuestas_correctas / total_preguntas) * 100 if total_preguntas > 0 else 0

            nueva_respuesta = Respuestas(
                nombreAlumno=nombre,
                apaternoAlumno=apaterno,
                respuesta='Examen Completo',
                grupo=alumno.grupo,
                calificacion=calificacion
            )
            db.session.add(nueva_respuesta)
            db.session.commit()

            return render_template('index.html', alumno=alumno, calificacion=calificacion)

    return render_template('examen.html', form=create_form)