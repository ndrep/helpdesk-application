import json, os
from .models import FrequenzaCorso, Ricevimento, Tag, Esame, Studente, CdL, Insegnamento, db
from  sqlalchemy.sql.expression import func
from random import randint
import datetime
from lorem.text import TextLorem


def load_db(json_path):
    with open(os.path.abspath(json_path)) as jf:
        data = json.load(jf)
      
    db.drop_all()
    db.create_all()

    #Insegnamenti
    insegnamenti = []
    for lista in data['insegnamenti']:
        key = Insegnamento(nome=lista['nome'], crediti=lista['crediti'], laboratorio=lista['laboratorio'], scritto=lista['scritto'], orale=lista['orale'], progetto=lista['progetto'])
        insegnamenti.append(key)
    db.session.add_all(insegnamenti)
    
    #CdL
    cdl = []
    for lista in data['facolta']:
        key = CdL(codice=lista['codice'], nome=lista['nome'], tipo=lista['tipo'])
        cdl.append(key)

    db.session.add_all(cdl)

    #Studente con CdL
    studenti = []
    for lista in data['studenti']:
        index = randint(1,5)
        key = Studente(email=lista['email'], nome=lista['nome'], cognome=lista['cognome'], matricola=lista['matricola'], anno_iscrizione=lista['anno_iscrizione'], cdl_id=index)
        studenti.append(key)
    
    db.session.add_all(studenti)

    esami = []
    for lista in data['esami']:
        key = Esame(data=datetime.datetime.strptime(lista['data'] , '%Y-%m-%d'), tipo_esame=lista['tipo_esame'], esito=lista['esito'], voto=lista['voto'], accettato=lista['accettato'], insegnamento_id=lista['insegnamento_id'], studente_id=lista['studente_id'])
        esami.append(key)
    
    db.session.add_all(esami)

    #Tag
    tag = []
    for lista in data['tag']:
        key = Tag(nome=lista['nome'])
        tag.append(key)

    db.session.add_all(tag)

    #Ricevimenti
    ricevimenti = []
    lorem = TextLorem(srange=(5,15))
    for lista in data['ricevimenti']:
        key = Ricevimento(data=datetime.datetime.strptime(lista['data'] , '%Y-%m-%d'), studente_id=lista['studente_id'], domande=lorem.sentence(), suggerimenti=lorem.sentence())
        key.tag.append(Tag.query.order_by(func.random()).first())
        ricevimenti.append(key)
    
    db.session.add_all(ricevimenti)

    #Frequenza Lezioni
    frequenze = []
    for lista in data['frequenza']:
        key = FrequenzaCorso(data=datetime.datetime.strptime(lista['data'] , '%Y-%m-%d'), studente_id=lista['studente_id'], insegnamento_id=lista['insegnamento_id'], presente=lista['presente'], anno_accademico=lista['anno_accademico'], tipo=lista['tipo'])
        frequenze.append(key)

    db.session.add_all(frequenze)

    db.session.commit()


