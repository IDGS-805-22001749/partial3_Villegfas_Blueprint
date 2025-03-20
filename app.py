from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Alumnos, Preguntas, Respuestas, User
from datetime import datetime, date
from forms import GrupoForm, LoginForm, RegistroForm
import forms
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, inicia sesión para continuar."
login_manager.login_message_category = "warning"

db.init_app(app)

# Ruta para el login (se asegura de que sea la página inicial)
# Ruta para el login (se asegura de que sea la página inicial)
@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Si ya estás autenticado, redirige directamente al index
        return redirect(url_for('index'))

    form = LoginForm()  # Instancia el formulario LoginForm
    
    if form.validate_on_submit():  # Verifica si el formulario es válido cuando se envía
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))  # Después de iniciar sesión, redirige al index
        else:
            flash('Usuario o contraseña incorrectos.')
    
    return render_template('login.html', form=form) 


@app.route("/index")
@login_required
def index():
    return render_template('index.html')


@app.route('/alumnos', methods=['GET', 'POST'])
@login_required
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


@app.route('/preguntas', methods=['GET','POST'])
@login_required
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
        return redirect(url_for('index'))

    return render_template('preguntas.html', form=create_form)


@app.route('/examen', methods=['GET', 'POST'])
@login_required
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


@app.route('/calificaciones', methods=['GET', 'POST'])
@login_required
def calificaciones():
    create_form = GrupoForm(request.form)
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    create_form.grupo.choices = [(grupo[0], grupo[0]) for grupo in grupos]

    alumnos = []
    grupo_seleccionado = None

    if request.method == 'POST' and create_form.validate_on_submit():
        grupo_seleccionado = create_form.grupo.data
        alumnos = db.session.query(Respuestas).filter_by(grupo=grupo_seleccionado).all()

    return render_template('calificaciones.html', form=create_form, alumnos=alumnos, grupo_seleccionado=grupo_seleccionado)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistroForm()  # Instancia el formulario RegistroForm

    if form.validate_on_submit():  # Si el formulario es válido
        username = form.username.data.strip()
        password = form.password.data.strip()
        
        # Verifica si el usuario ya existe en la base de datos
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Este nombre de usuario ya está registrado. Por favor elige otro.')
            return render_template('registro.html', form=form)

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        flash('Usuario registrado exitosamente.')
        return redirect(url_for('login'))  # Redirige al login después de registrar

    return render_template('registro.html', form=form)  # Pasa el formulario a la plantilla


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
