from app import app
from utils.db import db
from models.trabajador import Trabajador

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        db.session.commit()

        trabajadores = Trabajador.query.all()
        print(f" Conexión exitosa.")

    app.run(debug=True)
