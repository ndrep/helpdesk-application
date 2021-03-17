from backend.server.models import Studente, Esame

def test_string_check(client, app):
  with app.app_context():
    count = Studente.query.count()
    client.post(
      'new/?url=/',
      data={
        'email': 'prova.prova@studenti.unimi.it',
        'nome': '113',
        'cognome': '223'
        }
    )
    new_count = Studente.query.count()
    assert count == new_count
    client.post(
      'new/?url=/',
      data={
        'email': 'prova.prova@studenti.unimi.it',
        'nome': 'prova',
        'cognome': 'prova'
        }
    )
    new_count = Studente.query.count()
    assert new_count == count + 1

def test_result_check(client, app):
  with app.app_context():
    count = Esame.query.count()
    client.post(
      'esame/new/?url=/',
      data={
        'data': '2020-02-01',
        'tipo_esame': 'scritto',
        'esito': 'respinto',
        'voto': 23,
        'insegnamento': 1,
        'studente': 1
        }
    )
    new_count = Esame.query.count()
    assert new_count == count
    client.post(
      'esame/new/?url=/',
      data={
        'data': '2020-02-01',
        'tipo_esame': 'scritto',
        'esito': 'respinto',
        'insegnamento': 1,
        'studente': 1
        }
    )
    new_count = Esame.query.count()
    assert new_count == count + 1
