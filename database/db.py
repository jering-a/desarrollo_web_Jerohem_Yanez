from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
import enum

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()




# -------------------------------
class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)

    comunas = relationship("Comuna", back_populates="region", cascade="all, delete")


# -------------------------------
class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("Region", back_populates="comunas")
    actividades = relationship("Actividad", back_populates="comuna", cascade="all, delete")



# -------------------------------
class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    celular = Column(String(255), nullable=False)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=False)
    descripcion = Column(String(500), nullable=False)

    comuna = relationship("Comuna", back_populates="actividades")
    temas = relationship("ActividadTema", back_populates="actividad", cascade="all, delete")
    fotos = relationship("Foto", back_populates="actividad", cascade="all, delete")
    contactos = relationship("ContactarPor", back_populates="actividad", cascade="all, delete")

# -------------------------------
class TemaEnum(enum.Enum):
    musica = "música"
    deporte = "deporte"
    ciencias = "ciencias"
    religion = "religión"
    politica = "política"
    tecnologia = "tecnología"
    juegos = "juegos"
    baile = "baile"
    comida = "comida"
    otro = "otro"


class ActividadTema(Base):
    __tablename__ = 'actividad_tema'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum(TemaEnum), nullable=False)
    glosa_otro = Column(String(255))
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="temas")


# -------------------------------
class Foto(Base):
    __tablename__ = 'foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(255), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="fotos")

# -------------------------------
class ContactoEnum(enum.Enum):
    whatsapp = "whatsapp"
    telegram = "telegram"
    X = "X"
    instagram = "instagram"
    tiktok = "tiktok"
    otra = "otra"


class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum(ContactoEnum), nullable=False)
    identificador = Column(String(255), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="contactos")


def create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    new_actividad = Actividad(comuna_id=comuna_id, sector=sector, nombre=nombre, email=email, celular=celular, dia_hora_inicio=dia_hora_inicio, dia_hora_termino=dia_hora_termino, descripcion=descripcion)
    session.add(new_actividad)
    session.commit()
    actividad_id = new_actividad.id
    session.close()
    return actividad_id

def create_ActividadTema(tema, glosa_otro, actividad_id):
    session = SessionLocal()
    new_actividadTema = ActividadTema(tema=tema, glosa_otro=glosa_otro, actividad_id=actividad_id)
    session.add(new_actividadTema)
    session.commit()
    session.close()

def create_ContactarPor(nombre, identificador, actividad_id):
    session = SessionLocal()
    new_ContactarPor = ContactarPor(nombre=nombre, identificador=identificador, actividad_id=actividad_id)
    session.add(new_ContactarPor)
    session.commit()
    session.close()

def create_Foto(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    new_Foto= Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, actividad_id=actividad_id)
    session.add(new_Foto)
    session.commit()
    session.close()

def get_comuna_by_name(nombre):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(nombre=nombre).first()
    session.close()
    return comuna

def get_comuna_by_id(id):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(id=id).first()
    session.close()
    return comuna

def get_contacto_by_actividad_id(actividad_id):
    session = SessionLocal()
    contacto = session.query(ContactarPor).filter_by(actividad_id=actividad_id).first()
    session.close()
    return contacto

def get_foto_by_actividad_id(actividad_id):
    session = SessionLocal()
    foto = session.query(Foto).filter_by(actividad_id=actividad_id)
    session.close()
    return foto

def get_tema_by_actividad_id(actividad_id):
    session = SessionLocal()
    tema = session.query(ActividadTema).filter_by(actividad_id=actividad_id).first()
    session.close()
    return tema



def get_actividad_by_id(actividad_id):
    session = SessionLocal()
    actividad = session.query(Actividad)\
        .options(
            joinedload(Actividad.comuna),
            joinedload(Actividad.temas),
            joinedload(Actividad.contactos),
            joinedload(Actividad.fotos)
        )\
        .filter(Actividad.id == actividad_id)\
        .first()
    return actividad

