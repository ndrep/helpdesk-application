from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('tag_id', db.String, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('ricevimento_id', db.Integer, db.ForeignKey('ricevimento.id'), primary_key=True)
) 

class TipoEsame(enum.Enum):
    laboratorio = 'laboratorio'
    scritto = 'scritto'
    orale = 'orale'
    progetto = 'progetto'

class TipoLezione(enum.Enum):
    frontale = 'frontale'
    laboratorio = 'laboratorio'

class EsitoEsame(enum.Enum):
    respinto = 'respinto'
    approvato = 'approvato'

class Presenza(enum.Enum):
    A = 'A'
    P = 'P'
  
class Studente(db.Model):
    __tablename__ = 'studente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    cognome = db.Column(db.String(20), nullable=False)
    matricola = db.Column(db.String(6), unique=True)
    anno_iscrizione = db.Column(db.Integer())
    cdl_id = db.Column(db.String(20), db.ForeignKey('cdl.id'))
    evento = db.relationship('Evento',cascade='all', backref="studente")
    
    def __repr__(self):
        email = "%r" % (self.email)
        return email.replace("'","")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'nome': self.nome,
            'cognome': self.cognome,
            'matricola': self.matricola,
            'anno_iscrizione': self.anno_iscrizione,
        }

class CdL(db.Model):
    __tablename__ = 'cdl'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codice = db.Column(db.String(3), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    studente = db.relationship('Studente', backref="cdl")

    def __repr__(self):
        t = "%r  (%r)" % (self.nome, self.tipo)
        return t.replace("'","")

class Evento(db.Model):
    __tablename__= 'evento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date(), nullable=False)
    studente_id = db.Column(db.String(20), db.ForeignKey('studente.id'))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on':type,
    }

class Esame(Evento):
    __tablename__ = 'esame'
    id = db.Column(db.Integer(), db.ForeignKey('evento.id'), primary_key=True, autoincrement=True)
    tipo_esame = db.Column(db.Enum(TipoEsame), nullable=False)
    esito = db.Column(db.Enum(EsitoEsame), nullable=False)
    voto = db.Column(db.String())
    accettato = db.Column(db.Boolean())
    insegnamento_id = db.Column(db.String, db.ForeignKey('insegnamento.id'), nullable=False)


    __mapper_args__ = {
        'polymorphic_identity':'esame',
    }

class Ricevimento(Evento):
    __tablename__ = 'ricevimento'
    id = db.Column(db.Integer(), db.ForeignKey('evento.id'), primary_key=True, autoincrement=True)
    domande = db.Column(db.Text(200))
    suggerimenti = db.Column(db.Text(200))
    tag = db.relationship('Tag', secondary=tags)

    __mapper_args__ = {
        'polymorphic_identity':'ricevimento',
    }

    @property
    def serialize(self):
        return {
            'domande': self.domande,
            'suggerimenti': self.suggerimenti,
            'data': self.data.strftime("%Y-%m-%d"),
            'tag': self.serializeEventTag
        }
    
    @property
    def serializeEventTag(self):
       return [s.serialize for s in self.tag]
  
class FrequenzaCorso(Evento):
    __tablename__ = 'frequenza_corso'
    id = db.Column(db.Integer(), db.ForeignKey('evento.id'), primary_key=True, autoincrement=True)
    tipo = db.Column(db.Enum(TipoLezione), nullable=False)
    anno_accademico = db.Column(db.String(20), nullable=False)
    presente = db.Column(db.Enum(Presenza), nullable=False)
    insegnamento_id = db.Column(db.String, db.ForeignKey('insegnamento.id'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'frequenza_corso',
    }

class Insegnamento(db.Model):
    __tablename__ = 'insegnamento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    crediti = db.Column(db.Integer(), nullable=False)
    laboratorio = db.Column(db.Boolean(), nullable=False)
    scritto = db.Column(db.Boolean(), nullable=False)
    orale = db.Column(db.Boolean(), nullable=False)
    progetto = db.Column(db.Boolean(), nullable=False)
    esame = db.relationship('Esame', cascade='all,delete', backref='insegnamento')
    frq_corso = db.relationship('FrequenzaCorso', cascade='all,delete', backref='insegnamento')


    def __repr__(self):
        nome = "%r" % (self.nome)
        return nome.replace("'","")
    
    @property
    def serialize_attributes(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'crediti': self.crediti,
            'laboratorio': self.laboratorio,
            'scritto': self.scritto,
            'orale': self.orale,
            'progetto': self.progetto
        }
  
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    ricevimento = db.relationship('Ricevimento', secondary=tags)

    @property
    def serialize(self):
        return {
            'nome': self.nome
        }
    
