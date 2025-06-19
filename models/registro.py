# models/registro.py
from utils.db import db
from datetime import datetime

class RegistroHorario(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajador.id'))
    fecha = db.Column(db.Date)
    hora_entrada = db.Column(db.Time)
    hora_salida = db.Column(db.Time)
    dependencia = db.Column(db.String(3))  # D01, D02, D03

    trabajador = db.relationship('Trabajador', backref='registros')
