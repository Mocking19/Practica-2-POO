# app.py
from flask import Flask
from routes.control import control
from utils.db import db

app = Flask(__name__)
app.secret_key = "secreto123"  # Para usar flash

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(control)


