import re
from datetime import datetime


def validar_region_comuna(region, comuna):
    if not region or not comuna:
        return False, "Debe seleccionar una región y una comuna."
    return True, ""


def validar_sector(sector):
    if len(sector) > 100:
        return False, "El sector no puede exceder los 100 caracteres."
    return True, ""


def validar_nombre(nombre):
    if not nombre or len(nombre) > 200:
        return False, "Debe ingresar un nombre válido (máximo 200 caracteres)."
    return True, ""


def validar_email(email):
    patron = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"
    if not email or not re.match(patron, email) or len(email) > 100:
        return False, "Debe ingresar un email válido."
    return True, ""


def validar_telefono(telefono):
    if telefono and not re.match(r"^\+569\.\d{8}$", telefono):
        return False, "El número de celular debe tener el formato +569.12345678."
    return True, ""

def validar_contactar_por(contactar_por, contacto_id):
    if contactar_por and contacto_id:
        if len(contacto_id) < 4 or len(contacto_id) > 50:
            return False, "El ID o URL debe tener entre 4 y 50 caracteres."
    return True, ""


def validar_fecha_hora_inicio(fecha_inicio):
    try:
        datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
        return True, ""
    except ValueError:
        return False, f"La fecha y hora '{fecha_inicio}' no cumplen con el formato: año-mes-día hora:minuto (ejemplo: 2025-04-08 14:30)."


def validar_fecha_hora_termino(fecha_inicio, fecha_termino):
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
        termino = datetime.strptime(fecha_termino, "%Y-%m-%dT%H:%M")
        if termino <= inicio:
            return False, "La fecha y hora de término deben ser posteriores a la fecha y hora de inicio."
        return True, ""
    except ValueError:
        return False, "La fecha y hora de término no tienen un formato válido."


def validar_tema(tema, otro_tema):
    if not tema:
        return False, "Debe seleccionar un tema."
    if tema == "otro":
        if len(otro_tema) < 3 or len(otro_tema) > 15:
            return False, "El tema 'otro' debe tener entre 3 y 15 caracteres."
    return True, ""


def validar_fotos(files):
    fotos = files.getlist('fotos[]')
    if not fotos or all(f.filename == '' for f in fotos):
        return False, "Debes subir al menos una foto."
    if len(fotos) > 5:
        return False, "No puedes subir más de 5 fotos en total."
    return True, ""





   