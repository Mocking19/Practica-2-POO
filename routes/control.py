from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.trabajador import Trabajador
from models.registro import RegistroHorario
from utils.db import db
from datetime import datetime, date

control = Blueprint('control', __name__)

DEPENDENCIAS = {
    'D01': 'Edificio Central',
    'D02': 'Talleres',
    'D03': 'Centro Deportivo'
}

from sqlalchemy import func

@control.route("/")
def inicio():
    return render_template("inicio.html")

@control.route("/entrada", methods=["GET", "POST"])
def registrar_entrada():
    if request.method == "POST":
        legajo = request.form.get("legajo", "").strip()
        ultimos_4_dni = request.form.get("dni", "").strip()
        dependencia_codigo = request.form.get("dependencia", "").strip()

        if not legajo or not ultimos_4_dni:
            flash("Campos incompletos", "error")
            return redirect(url_for("control.registrar_entrada"))

        print(f"Legajo recibido (tipo {type(legajo)}): [{legajo}]")

        trabajador = Trabajador.query.filter(
            func.trim(Trabajador.legajo) == legajo
        ).first()

        if not trabajador:
            flash("Legajo no encontrado", "error")
            return redirect(url_for("control.registrar_entrada"))

        if not trabajador.dni.endswith(ultimos_4_dni):
            flash("Últimos 4 dígitos del DNI incorrectos", "error")
            return redirect(url_for("control.registrar_entrada"))

        hoy = date.today()
        registro_existente = RegistroHorario.query.filter_by(
            trabajador_id=trabajador.id, fecha=hoy).first()

        if registro_existente:
            flash("Ya hay una entrada registrada para hoy", "warning")
            return redirect(url_for("control.registrar_entrada"))

        nuevo_registro = RegistroHorario(
            trabajador_id=trabajador.id,
            fecha=hoy,
            hora_entrada=datetime.now().time(),
            dependencia=dependencia_codigo
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        flash("Entrada registrada correctamente", "success")
        return redirect(url_for("control.registrar_entrada"))

    return render_template("entrada.html", dependencias=DEPENDENCIAS)




@control.route("/salida", methods=["GET", "POST"])
def registrar_salida():
    if request.method == "POST":
        legajo = request.form.get('legajo', '').strip()
        ultimos_4_dni = request.form.get('dni', '').strip()

        try:
            legajo_int = int(legajo)
            print(f"Legajo recibido (tipo {type(legajo_int)}): {legajo_int}")
        except ValueError:
            flash("Legajo inválido", "error")
            return redirect(url_for("control.registrar_entrada"))

        trabajador = Trabajador.query.filter_by(legajo=legajo_int).first()


        if not trabajador:
            flash("Legajo no encontrado", "error")
            return redirect(url_for("control.registrar_salida"))

        if not trabajador.dni.endswith(ultimos_4_dni):
            flash("Últimos 4 dígitos del DNI incorrectos", "error")
            return redirect(url_for("control.registrar_salida"))

        hoy = date.today()
        registro = RegistroHorario.query.filter_by(trabajador_id=trabajador.id, fecha=hoy).first()

        if not registro:
            flash("No hay una entrada registrada hoy", "warning")
            return redirect(url_for("control.registrar_salida"))

        if registro.hora_salida is not None:
            flash("Ya se registró la salida para hoy", "info")
            return redirect(url_for("control.registrar_salida"))

        registro.hora_salida = datetime.now().time()
        db.session.commit()
        flash(f"Salida registrada para la dependencia {registro.dependencia}", "success")
        return redirect(url_for("control.registrar_salida"))

    # GET
    return render_template("salida.html")


@control.route("/consultar", methods=["GET", "POST"])
def consultar_registros():
    registros = []
    if request.method == "POST":
        legajo = request.form.get('legajo', '').strip()
        ultimos_4_dni = request.form.get('dni', '').strip()
        desde = request.form.get('desde', '').strip()
        hasta = request.form.get('hasta', '').strip()

        try:
            legajo_int = int(legajo)
            print(f"Legajo recibido (tipo {type(legajo_int)}): {legajo_int}")
        except ValueError:
            flash("Legajo inválido", "error")
            return redirect(url_for("control.registrar_entrada"))

        trabajador = Trabajador.query.filter_by(legajo=legajo_int).first()

        if not trabajador:
            flash("Legajo no encontrado", "error")
        elif not trabajador.dni.endswith(ultimos_4_dni):
            flash("Últimos 4 dígitos del DNI incorrectos", "error")
        else:
            try:
                registros = RegistroHorario.query.filter(
                    RegistroHorario.trabajador_id == trabajador.id,
                    RegistroHorario.fecha >= desde,
                    RegistroHorario.fecha <= hasta
                ).order_by(RegistroHorario.fecha.asc()).all()
            except Exception as e:
                flash("Error en las fechas ingresadas o consulta.", "error")

    return render_template("consultar.html", registros=registros, dependencias=DEPENDENCIAS)

