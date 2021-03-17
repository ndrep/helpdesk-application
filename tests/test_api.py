from flask import json

def test_lista_iscrizioni(client):
  response = client.get('/api/anno_iscrizione').get_data(as_text=True)
  studenti = json.loads(response)
  assert studenti is not None
  assert studenti[0]['value'] is not None
  assert studenti[0]['label'] is not None

def test_totale_studenti(client):
  response = client.get('/api/totale_studenti?cognome=&iscrizione=').get_data(as_text=True)
  studenti = json.loads(response)
  assert studenti is not None
  assert studenti == 30

def test_esami_superati_studente(client):
  response = client.get('/api/esami_superati_studente?id=1').get_data(as_text=True)
  esami = json.loads(response)
  assert esami['json_list'] is not None
  assert isinstance(esami['json_list'][0]['voto'],str)
  assert esami['json_list'][0]['esito'] == 'approvato'
  assert esami['json_list'][0]['accettato'] is not None

def test_statistiche_studente(client):
  response = client.get('/api/statistiche_studente?id=9').get_data(as_text=True)
  stat = json.loads(response)
  assert stat['json_list'] is not None
  assert stat['json_list'][0]['esame'] == 'SISTEMI OPERATIVI'
  assert isinstance(stat['json_list'][0]['tentativi'],int)
  assert stat['json_list'][0]['tipo'] == 'laboratorio'
  assert stat['json_list'][0]['voto'] == '18'

def test_lista_anni_per_esame(client):
  response = client.get('/api/appelli?insegnamento=SISTEMI%20OPERATIVI&tipo=laboratorio').get_data(as_text=True)
  appelli = json.loads(response)
  assert appelli['json_list'] is not None
  assert appelli['json_list'][0] == '2020'

def test_lista_esami(client):
  response = client.get('/api/date_appelli?insegnamento=SISTEMI%20OPERATIVI&tipo=laboratorio&anno=2020').get_data(as_text=True)
  esami_anno = json.loads(response)
  assert esami_anno['json_list'] is not None
  assert esami_anno['json_list'][0] == '2020-01-20'

def test_lista_tipo_esame(client):
  response = client.get('/api/modalita_esame?insegnamento=PROGRAMMAZIONE').get_data(as_text=True)
  tipi = json.loads(response)
  assert tipi['json_list'] is not None
  assert tipi['json_list'][0] == 'laboratorio'
  assert tipi['json_list'][1] == 'scritto'
  assert tipi['json_list'][2] == 'orale'
  response = client.get('/api/modalita_esame?insegnamento=LINGUAGGI%20E%20TRADUTTORI').get_data(as_text=True)
  tipi = json.loads(response)
  assert tipi['json_list'][0] == 'orale'
  assert tipi['json_list'][1] == 'progetto'

def test_lista_insegnamenti(client):
  response = client.get('/api/insegnamenti').get_data(as_text=True)
  insegnamenti = json.loads(response)
  assert insegnamenti is not None
  assert len(insegnamenti) == 4

def test_risultati_esame(client):
  response = client.get('/api/risultati_esame?insegnamento=SISTEMI%20OPERATIVI&tipo=laboratorio&data=2020-01-20').get_data(as_text=True)
  risultati = json.loads(response)
  assert risultati['json_list'] is not None
  assert len(risultati['json_list']) == 30

def test_lista_ricevimenti_studente(client):
  response = client.get('/api/lista_ricevimenti?email=qmullins0@studenti.unimi.it').get_data(as_text=True)
  ricevimenti = json.loads(response)
  assert ricevimenti is not None
  assert len(ricevimenti) == 6
  response = client.get('/api/lista_ricevimenti?page=0').get_data(as_text=True)
  ricevimenti = json.loads(response)
  assert len(ricevimenti) == 14


def test_lista_studenti(client):
  response = client.get('/api/lista_studenti').get_data(as_text=True)
  studenti = json.loads(response)
  assert studenti is not None
  assert studenti[0]['label'] == studenti[0]['value']

def test_totale_ricevimenti(client):
  response = client.get('/api/totale_ricevimenti?email=&tag=').get_data(as_text=True)
  number = json.loads(response)
  assert number is not None
  assert isinstance(number,int)

def test_lista_tag(client):
  response = client.get('/api/lista_tag').get_data(as_text=True)
  tag = json.loads(response)
  assert tag is not None
  assert tag[0]['text'] == tag[0]['value']

def test_lista_presenze_corso(client):
  response = client.get('/api/lista_presenze_corso?insegnamento=programmazione&anno_accademico=2019/2020&tipo=laboratorio').get_data(as_text=True)
  studenti = json.loads(response)
  assert len(studenti) == 5
  assert isinstance(studenti[0]['presenze'],int)
  assert isinstance(studenti[0]['totale'],int)

def test_lista_anni_accademici(client):
  response = client.get('/api/lista_anni_accademici?insegnamento=programmazione').get_data(as_text=True)
  lista = json.loads(response)
  assert len(lista) == 1
  assert '2019/2020' in lista

def test_tipo_lezione(client):
  response = client.get('/api/tipo_lezione?insegnamento=programmazione&anno_accademico=2019/2020').get_data(as_text=True)
  tipo = json.loads(response)
  assert tipo is not None
  assert 'laboratorio' in tipo or 'frontale' in tipo

def test_date_presenze(client):
  response = client.get('/api/date_presenze?insegnamento=programmazione&anno_accademico=2019/2020&tipo=laboratorio&studente_id=1').get_data(as_text=True)
  date = json.loads(response)
  assert date is not None
  assert isinstance(date[0]['presenza'],str)
  assert isinstance(date[0]['data'],str)

def test_lista_studenti_tot(client):
  response = client.get('/api/studente?cognome=mu&iscrizione=2016').get_data(as_text=True)
  studenti = json.loads(response)
  assert studenti['json_list'] is not None
  assert studenti['json_list'][0]['cognome'] == 'Mullins'
  response = client.get('/api/studente?page=0').get_data(as_text=True)
  studenti = json.loads(response)
  assert len(studenti['json_list']) == 14

  





