import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Adresse(Base):
    __tablename__ = 'Adresse'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Plz = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    ortsname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Strasse = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Hausnr = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

class Person(Base):
    __tablename__ = 'Person'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Adresse = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Adresse.id'), nullable=False)
    Name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Geburtsdatum = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    Titel = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

class Unternehmen(Base):
    __tablename__ = 'Unternehmen'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Adresse = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Adresse.id'), nullable=False)
    Umsatz = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

class Kontakt(Base):
    __tablename__ = 'Kontakt'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    EMail = sqlalchemy.Column('E-Mail', sqlalchemy.String(255), nullable=False)
    Telefonnummer = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Rolle = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Referenz = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    RefTyp = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

class Terminart(Base):
    __tablename__ = 'Terminart'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

class Termine(Base):
    __tablename__ = 'Termine'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Titel = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Ort = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Art = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Terminart.id'), nullable=False)
    Start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    Ende = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    Uid = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

class Protokoll(Base):
    __tablename__ = 'Protokoll'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Datum = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    Text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    Dauer = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    TLDR = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Termin = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Termine.id'), nullable=False)

class Teilnehmer(Base):
    __tablename__ = 'Teilnehmer'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Kontakt = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Kontakt.id'), nullable=False)
    Termin = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Termine.id'), nullable=False)

class Medium(Base):
    __tablename__ = 'Medium'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Dateityp = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Dateiname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

class Anhang(Base):
    __tablename__ = 'Anhang'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Protokoll = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Protokoll.id'), nullable=False)
    Medium = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Medium.id'), nullable=False)

class Produkt(Base):
    __tablename__ = 'Produkt'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Bezeichnung = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    Preis = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)

class Wichtigkeit(Base):
    __tablename__ = 'Wichtigkeit'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    level = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

class Auftrag(Base):
    __tablename__ = 'Auftrag'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Bezeichnung = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    wichtigkeit = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Wichtigkeit.id'), nullable=True)
    Kontakt = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Kontakt.id'), nullable=False)

class Auftragsposition(Base):
    __tablename__ = 'Auftragsposition'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Auftrag = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Auftrag.id'), nullable=False)
    Produkt = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Produkt.id'), nullable=False)

