# models.py
from flask_sqlalchemy import SQLAlchemy 
import datetime 
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    amaterno = db.Column(db.String(50))
    fechaNacimiento = db.Column(db.Date)
    edad = db.Column(db.Integer)
    grupo = db.Column(db.String(10))
   
class Profesores(db.Model):
    __tablename__ = 'profesores'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apaterno=db.Column(db.String(50))
    email=db.Column(db.String(50))

class Preguntas(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(50))
    pregunta = db.Column(db.String(200))
    a = db.Column(db.String(100))
    b = db.Column(db.String(100))
    c = db.Column(db.String(100))
    d = db.Column(db.String(100))
    respuestaCorrecta = db.Column(db.String(1))
    

class Respuestas(db.Model):
    __tablename__ = 'respuestas'
    id = db.Column(db.Integer, primary_key=True)
    nombreAlumno = db.Column(db.String(100))
    apaternoAlumno = db.Column(db.String(100))
    respuesta = db.Column(db.String(50))
    grupo = db.Column(db.String(10))
    calificacion = db.Column(db.Float)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False) 
    

