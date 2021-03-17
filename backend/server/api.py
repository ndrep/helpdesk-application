from flask import Blueprint, jsonify, request, json
from .models import Studente, Ricevimento, Tag, Esame, Insegnamento, CdL, FrequenzaCorso

api = Blueprint('api', __name__)

@api.route('/anno_iscrizione')
def lista_iscrizioni():
    iscrizioni = [e.serialize for e in Studente.query.distinct(Studente.anno_iscrizione).group_by(Studente.anno_iscrizione)]
    options = []
    for i in iscrizioni:
        options.append({
            'value': i['anno_iscrizione'],
            'label': i['anno_iscrizione']
            })
        
    return jsonify(options)

@api.route('/totale_studenti')
def totale_studenti():
    studenti = Studente.query
    cognome = request.args.get('cognome')
    if cognome is not None and cognome != '':
        studenti = studenti.filter(Studente.cognome.contains(cognome.strip()))
    anno = request.args.get('iscrizione')
    if anno is not None and anno != '':
        studenti = studenti.filter(Studente.anno_iscrizione == anno)
    return jsonify(studenti.count())

@api.route('/studente')
def lista_studenti():
    studenti = Studente.query.order_by(Studente.cognome.asc())
    lista = []
    cognome = request.args.get('cognome')
    if cognome is not None and cognome != '':
        studenti = studenti.filter(Studente.cognome.contains(cognome.strip()))
    anno = request.args.get('iscrizione')
    if anno is not None and anno != '':
        studenti = studenti.filter(Studente.anno_iscrizione == anno)
    page = request.args.get('page')
    if page is not None:
        page = int(page)
        studenti = studenti.limit(14).offset(page*14)
    for e in studenti:
        insegnamento = CdL.query.filter(CdL.id==e.cdl_id).with_entities(CdL.nome).first()
        lista.append({
            'id': e.id,
            'email': e.email,
            'nome': e.nome,
            'cognome': e.cognome,
            'matricola': e.matricola,
            'anno_iscrizione': e.anno_iscrizione,
            'facolta': insegnamento[0]
        })
    
    return jsonify(json_list=lista)


@api.route('/esami_superati_studente')
def lista_esami_superati_studente():
    studente_id = request.args.get('id')
    lista = []
    for esame in Esame.query.filter(Esame.studente_id==studente_id, Esame.esito=='approvato', Esame.accettato==True).join(Insegnamento).with_entities(Esame.voto, Esame.data, Esame.accettato, Esame.tipo_esame, Esame.esito, Insegnamento.nome).all():
        lista.append({
            'data': esame.data.strftime("%Y-%m-%d"),
            'tipo_esame': json.dumps(esame.tipo_esame, default=str).replace("\"TipoEsame.","").replace("\"",""),
            'esito': json.dumps(esame.esito, default=str).replace("\"EsitoEsame.","").replace("\"",""),
            'voto': esame.voto,
            'accettato': esame.accettato,
            'insegnamento': esame.nome
        })
    return jsonify(json_list=lista)
    

@api.route('/statistiche_studente')
def statistiche_studente():
    corsi = Insegnamento.query.all()
    studente_id = request.args.get('id')
    tipo = []
    lista = []
    for c in corsi:
        getListOfExam(c.nome, tipo)
        for t in tipo:
            tentativi = Esame.query.filter_by(studente_id=studente_id, esito='respinto', tipo_esame=t).join(Insegnamento).filter(Insegnamento.nome==c.nome).count()
            lista.append({
                'esame': c.nome,
                'tipo': t,
                'tentativi': tentativi
            })
            esame = Esame.query.filter(Esame.studente_id==studente_id, Esame.esito=='approvato', Esame.accettato==False, Esame.tipo_esame==t).join(Insegnamento).filter(Insegnamento.nome==c.nome).with_entities(Esame.voto, Esame.data).order_by(Esame.data.desc()).first()
            if(esame):
                for data in lista:
                    if(c.nome in data.values() and t in data.values()):
                        data.update({
                            'data_rifiuto': esame.data.strftime("%Y-%m-%d"),
                            'voto': esame.voto
                        })  
        tipo.clear()
    new_lista = []
    for l in lista:
        if (len(l) == 3 and l['tentativi'] != 0) or len(l) == 5:
            new_lista.append(l) 

    return jsonify(json_list=new_lista)

def getListOfExam(c, tipo):
    if Insegnamento.query.filter_by(nome=c ,laboratorio=True).all():
        tipo.append('laboratorio')
    if Insegnamento.query.filter_by(nome=c,scritto=True).all():
        tipo.append('scritto')
    if Insegnamento.query.filter_by(nome=c,orale=True).all():
        tipo.append('orale')
    if Insegnamento.query.filter_by(nome=c,progetto=True).all():
        tipo.append('progetto')

@api.route('/appelli')
def lista_anni_per_esame():
    nome = request.args.get('insegnamento')
    tipo = request.args.get('tipo')
    anni = Esame.query.filter(Esame.tipo_esame==tipo).join(Insegnamento).filter(Insegnamento.nome==nome).distinct(Esame.data).group_by(Esame.data)
    lista = []
    for a in anni:
        if(a.data.strftime("%Y") not in lista):
            lista.append(a.data.strftime("%Y"))
    return jsonify(json_list=lista)

@api.route('/date_appelli')
def lista_esami():
    nome = request.args.get('insegnamento')
    tipo = request.args.get('tipo')
    anno = request.args.get('anno')
    esami = Esame.query.filter(Esame.tipo_esame==tipo, Esame.data.contains(anno)).join(Insegnamento).filter(Insegnamento.nome==nome).distinct(Esame.data).group_by(Esame.data)
    lista = []
    for e in esami:
        lista.append(e.data.strftime("%Y-%m-%d"))
    return jsonify(json_list=lista)

@api.route('/modalita_esame')
def lista_tipo_esame():
    nome = request.args.get('insegnamento')
    corso = [t.serialize_attributes for t in Insegnamento.query.filter_by(nome=nome.upper()).all()]
    attributes = []
    if corso[0].get('laboratorio') == True:
        attributes.append('laboratorio')
    if corso[0].get('scritto') == True:
        attributes.append('scritto')
    if corso[0].get('orale') == True:
        attributes.append('orale')
    if corso[0].get('progetto') == True:
        attributes.append('progetto')
    return jsonify(json_list=attributes)

@api.route('/insegnamenti')
def lista_insegnamenti():
    lista = []
    for i in Insegnamento.query.all():
        lista.append(i.nome)
    return jsonify(lista)

@api.route('/risultati_esame')
def lista_risultati_esame():
    nome = request.args.get('insegnamento')
    tipo = request.args.get('tipo')
    data = request.args.get('data')
    esami = Esame.query.filter(Esame.tipo_esame==tipo, Esame.data==data).join(Insegnamento).filter(Insegnamento.nome==nome).all()
    lista = []
    for esame in esami:
        listOfResult(esame, lista)
    return jsonify(json_list=lista) 

def listOfResult(esame, lista):
    studente = Studente.query.filter_by(id=esame.studente_id).all()
    lista.append({
        'esito': json.dumps(esame.esito, default=str).replace("\"EsitoEsame.","").replace("\"",""),
        'voto': esame.voto,
        'nome': studente[0].nome,
        'cognome': studente[0].cognome,
        'matricola': studente[0].matricola

    })

@api.route('/lista_ricevimenti')
def lista_ricevimenti():
    lista = []
    ricevimenti = Ricevimento.query.order_by(Ricevimento.data.desc())
    email = request.args.get('email')
    if email is not None and email != '':
        ricevimenti = ricevimenti.join(Studente).filter(Studente.email==email).order_by(Ricevimento.data.desc())
    tag = request.args.get('tag')
    if tag is not None and tag != '': 
        tag = tag.split(',')
        ricevimenti = ricevimenti.join(Tag, Ricevimento.tag).filter(Tag.nome.in_(tag)).order_by(Ricevimento.data.desc())
    page = request.args.get('page')
    if page is not None and page != '':
        page = int(page)
        ricevimenti = ricevimenti.limit(14).offset(page*14)
    for ricevimento in ricevimenti:
        lista.append(ricevimento.serialize)
        studente = Studente.query.join(Ricevimento).filter(Ricevimento.studente_id==ricevimento.studente_id).with_entities(Studente.nome, Studente.cognome).first()
        lista[-1].update({
            'nome': studente.nome,
            'cognome': studente.cognome
        })  
    return jsonify(lista)

@api.route('/lista_studenti')
def lista_studenti_ricevimento():
    studenti = Studente.query.all()
    lista = []
    for studente in studenti:
        lista.append({
            'value': studente.email,
            'label': studente.email,
        })
    return jsonify(lista)

@api.route('/totale_ricevimenti')
def totale_ricevimenti():
    ricevimenti = Ricevimento.query.order_by(Ricevimento.data.desc())
    email = request.args.get('email')
    if email is not None and email != '':
        ricevimenti = ricevimenti.join(Studente).filter(Studente.email==email).order_by(Ricevimento.data.desc())
    tag = request.args.get('tag')
    if tag is not None and tag != '': 
        tag = tag.split(',')
        ricevimenti = ricevimenti.join(Tag, Ricevimento.tag).filter(Tag.nome.in_(tag)).order_by(Ricevimento.data.desc())
    return jsonify(ricevimenti.count())

@api.route('/lista_tag')
def lista_tag():
    lista = []
    tags = Tag.query.filter(Tag.ricevimento!=None).all()
    for tag in tags:
        lista.append({
            'value': tag.nome,
            'text': tag.nome
        })
    return jsonify(lista)

@api.route('/lista_presenze_corso')
def lista_presenze():
    lista = []
    columns = []
    corso = request.args.get('insegnamento')
    anno = request.args.get('anno_accademico')
    tipo = request.args.get('tipo')
    studenti = FrequenzaCorso.query.filter(FrequenzaCorso.anno_accademico==anno, FrequenzaCorso.tipo==tipo).join(Insegnamento).filter(Insegnamento.nome==corso.upper()).join(Studente).with_entities(FrequenzaCorso.anno_accademico, FrequenzaCorso.tipo, Studente.nome, Studente.cognome, Studente.id).distinct(Studente.matricola).group_by(Studente.matricola)
    for studente in studenti:
        lista.append({
            'nome': studente.nome,
            'cognome': studente.cognome,
            'insegnamento': corso,
            'studente_id': studente.id
        })
    
    for studente in lista:
        presenze = FrequenzaCorso.query.filter(FrequenzaCorso.anno_accademico==anno, FrequenzaCorso.presente=="P", FrequenzaCorso.tipo==tipo).join(Insegnamento).filter(Insegnamento.nome==corso.upper()).join(Studente).filter(Studente.id==studente['studente_id']).count()
        totale = FrequenzaCorso.query.filter(FrequenzaCorso.anno_accademico==anno, FrequenzaCorso.tipo==tipo).join(Insegnamento).filter(Insegnamento.nome==corso.upper()).join(Studente).filter(Studente.id==studente['studente_id']).count()
        studente.update({
            'presenze': presenze,
            'totale': totale
        })

    return jsonify(lista)

@api.route('/lista_anni_accademici')
def lista_anni_accademici():
    corso = request.args.get('insegnamento')
    lista = []
    anni_accademici = FrequenzaCorso.query.join(Insegnamento).filter(Insegnamento.nome==corso.upper()).distinct(FrequenzaCorso.anno_accademico).group_by(FrequenzaCorso.anno_accademico)
    for anno in anni_accademici:
        lista.append(anno.anno_accademico)
    return jsonify(lista)

@api.route('/tipo_lezione')
def lista_tipi_lezione():
    corso = request.args.get('insegnamento')
    anno = request.args.get('anno_accademico')
    lista = []
    tipi = FrequenzaCorso.query.filter(FrequenzaCorso.anno_accademico==anno).join(Insegnamento).filter(Insegnamento.nome==corso.upper()).distinct(FrequenzaCorso.tipo).group_by(FrequenzaCorso.tipo)
    for tipo in tipi:
        lista.append(json.dumps(tipo.tipo, default=str).replace("\"TipoLezione.","").replace("\"",""))
    return jsonify(lista)

@api.route('/date_presenze')
def lista_date_presenze():
    lista = []
    corso = request.args.get('insegnamento')
    anno = request.args.get('anno_accademico')
    tipo = request.args.get('tipo')
    studente_id = request.args.get('studente_id')
    date = FrequenzaCorso.query.filter(FrequenzaCorso.tipo==tipo, FrequenzaCorso.anno_accademico==anno).join(Insegnamento).filter(Insegnamento.nome==corso.upper()).join(Studente).filter(Studente.id==studente_id)
    for data in date:
        lista.append({
            'data': data.data.strftime("%Y-%m-%d"),
            'presenza': json.dumps(data.presente, default=str).replace("\"Presenza.","").replace("\"","")
        })
    return jsonify(lista)





    



