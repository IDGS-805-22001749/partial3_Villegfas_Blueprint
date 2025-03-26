# forms.py

from wtforms import Form

from flask_wtf import FlaskForm

 

from wtforms import StringField,IntegerField,SelectField,RadioField,PasswordField

from wtforms import EmailField

from wtforms import validators 
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp



class FormsAlumno(FlaskForm):

    id=IntegerField('id', [
        validators.number_range(min=1, max=20,message='valor no valido')
     
    ])

    nombre=StringField('Nombre',[

        validators.DataRequired(message='El nombre es requerido'),

        validators.length(min=4,max=20, message='requiere min=4 max=20')

    ])

    apaterno=StringField('Apellido Paterno',[

        validators.DataRequired(message='El apellido es requerido')

    ])

    amaterno=StringField('Apellido Materno',[

        validators.DataRequired(message='El campo es requerido'),

        validators.length(min=4,max=10, message='ingresa un apellido valido')

    ])

    dia = IntegerField('Día', [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1, max=31, message='El día debe estar entre 1 y 31')
    ])

    mes = IntegerField('Mes', [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1, max=12, message='El mes debe estar entre 1 y 12')
    ])

    anio = IntegerField('Año', [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1900, max=2025, message='El año debe ser válido')
    ])
    
    grupo=StringField('Grupo',[

        validators.DataRequired(message='El campo es requerido'),

        validators.length(min=4,max=10, message='ingresa un grupo valido')

    ])






class FormPreguntas(FlaskForm):
    materia = SelectField('Materia', 
        choices=[
            ('matematicas', 'Matemáticas'),
            ('historia', 'Historia'),
            ('ciencias', 'Ciencias'),
            ('literatura', 'Literatura')
        ],
        validators=[DataRequired(message='El campo es requerido')]
    )
   
    pregunta = StringField('Pregunta', validators=[
        DataRequired(message='El campo es requerido')
    ])
    
    a = StringField('Opción A', validators=[
        DataRequired(message='El campo es requerido')
    ])
    
    b = StringField('Opción B', validators=[
        DataRequired(message='El campo es requerido')
    ])
    
    c = StringField('Opción C', validators=[
        DataRequired(message='El campo es requerido')
    ])
    
    d = StringField('Opción D', validators=[
        DataRequired(message='El campo es requerido')
    ])
    
    respuestaCorrecta = RadioField('Selecciona la respuesta correcta:', 
        choices=[
            ('a', 'Opción A'),
            ('b', 'Opción B'),
            ('c', 'Opción C'),
            ('d', 'Opción D')
        ],
        validators=[DataRequired(message='Selecciona la respuesta correcta')]
    )
    
    

class GrupoForm(FlaskForm):
    grupo = SelectField('Grupo', choices=[])



class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message='El campo es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='El campo es requerido')])


class RegistroForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[
            DataRequired(message='El campo es requerido'),
            Length(min=3, max=16, message='El usuario debe tener entre 3 y 16 caracteres'),
            Regexp(r'^[a-zA-Z0-9_]+$', message='El usuario solo puede contener letras, números y guiones bajos')
        ]
    )
    password = PasswordField(
    'Contraseña',
    validators=[
        DataRequired(message='El campo es requerido'),  
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres'),  
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&]{8,}$', message='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial @$!%*?&#')
    ]
    )
    role = SelectField('Rol', 
        choices=[
            ('alumno', 'Alumno'),
            ('profesor', 'Profesor'),
        ],
        validators=[DataRequired(message='El campo es requerido')]
    )


class FormProfesores(FlaskForm):
    
    id=IntegerField('id',

    [validators.number_range(min=1, max=20,message='valor no valido')])

    nombre=StringField('Nombre',[

        validators.DataRequired(message='El nombre es requerido'),

        validators.length(min=4,max=20, message='requiere min=4 max=20')

    ])
    apaterno=StringField('Apellido',[

        validators.DataRequired(message='El apellido es requerido')

    ])

    email=EmailField('Correo',[

        validators.DataRequired(message='El apellido es requerido'),

        validators.Email(message='Ingrese un correo valido')

    ])