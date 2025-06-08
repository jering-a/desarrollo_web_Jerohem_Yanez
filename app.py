import os
from flask import Flask, request, render_template, redirect, url_for, session
from database import db
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from utils.validations import validar_contactar_por, validar_email, validar_fecha_hora_inicio, validar_fecha_hora_termino, validar_fotos, validar_nombre, validar_region_comuna, validar_sector, validar_telefono, validar_tema

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/actividades", methods=["GET"])
def actividades():
    pagina = request.args.get('pagina', default=1, type=int)
    actividades_por_pagina = 5

    session = db.SessionLocal()
    total_actividades = session.query(db.Actividad).count()
    total_paginas = (total_actividades + actividades_por_pagina - 1) // actividades_por_pagina

    actividades = session.query(db.Actividad) \
        .options(
            joinedload(db.Actividad.comuna),
            joinedload(db.Actividad.temas),
            joinedload(db.Actividad.fotos),
            joinedload(db.Actividad.contactos)
        ) \
        .order_by(db.Actividad.dia_hora_inicio.desc()) \
        .offset((pagina - 1) * actividades_por_pagina) \
        .limit(actividades_por_pagina) \
        .all()

    session.close()

    return render_template("actividades.html",
                           actividades=actividades,
                           pagina=pagina,
                           total_paginas=total_paginas)



@app.route("/actividad/<int:actividad_id>", methods=["GET"])
def actividad(actividad_id):
    actividad = db.get_actividad_by_id(actividad_id)
    return render_template('actividad.html',
                           actividad=actividad)


@app.route('/agregar', methods=["GET", "POST"])
def agregar():
    error = None
    mensaje = None
    if request.method == "POST":
        valido, errores = validar_formulario(request)
        if not valido:
            error= errores
        else:
            insertar_tablas(request)   
            mensaje= "Agregado correctamente"
    return render_template("agregarActividad.html", mensaje=mensaje, error=error)



@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("estadisticas.html")

def insertar_tablas(req):
    region = req.form.get('region')
    comuna = req.form.get('comuna')
    sector = req.form.get('sector', '')
    nombre = req.form.get('nombre')
    email = req.form.get('email')
    telefono = req.form.get('celular', '')
    contactar_por = req.form.get('contacto', '')
    contacto_id = req.form.get('contactoInfo', '')
    fecha_inicio = req.form.get('inicio')
    fecha_termino = req.form.get('termino')
    tema = req.form.get('tema')
    otro_tema = req.form.get('temaOtro', '')
    descripcion = req.form.get('descripcion')
    fotos = req.files.getlist('fotos[]')
    comuna_id = db.get_comuna_by_name(comuna).id

    actividad_id = db.create_actividad(comuna_id, sector, nombre, email, telefono, fecha_inicio, fecha_termino, descripcion)
    db.create_ActividadTema(tema, otro_tema, actividad_id)
    db.create_ContactarPor(contactar_por, contacto_id, actividad_id)
    for foto in fotos:
        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            foto.save(save_path)

            # URL relativa para acceder desde el navegador
            url = f"/{UPLOAD_FOLDER}/{filename}"

        # Guarda en la base de datos
        db.create_Foto(url, filename, actividad_id)




def validar_formulario(req):
    errores = []

    region = req.form.get('region')
    comuna = req.form.get('comuna')
    sector = req.form.get('sector', '')
    nombre = req.form.get('nombre')
    email = req.form.get('email')
    telefono = req.form.get('celular', '')
    contactar_por = req.form.get('contacto', '')
    contacto_id = req.form.get('contactoInfo', '')
    fecha_inicio = req.form.get('inicio')
    fecha_termino = req.form.get('termino')
    tema = req.form.get('tema')
    otro_tema = req.form.get('temaOtro', '')
    fotos = req.files

    # Validaciones
    validadores = [
        validar_region_comuna(region, comuna),
        validar_sector(sector),
        validar_nombre(nombre),
        validar_email(email),
        validar_telefono(telefono),
        validar_contactar_por(contactar_por, contacto_id),
        validar_fecha_hora_inicio(fecha_inicio),
        validar_fecha_hora_termino(fecha_inicio, fecha_termino),
        validar_tema(tema, otro_tema),
        validar_fotos(fotos)
    ]

    for valido, mensaje in validadores:
        if not valido:
            errores.append(mensaje)

    return len(errores) == 0, errores


if __name__ == "__main__":
    app.run(debug=True)

