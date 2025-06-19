# models/trabajador.py
from utils.db import db

class Trabajador(db.Model):
    __tablename__ = 'trabajador'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    dni = db.Column(db.String(8))
    correo = db.Column(db.String(100))
    legajo = db.Column(db.String(10), unique=True)
    horas_semanales = db.Column(db.Integer)
    funcion = db.Column(db.String(2))  # DO, AD, TE

    def verificar_identidad(self, legajo_input, ultimos_4_dni):
        return self.legajo == legajo_input and self.dni[-4:] == ultimos_4_dni

        