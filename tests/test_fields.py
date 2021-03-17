from backend.server.models import Tag, Ricevimento

def test_advanced_tag_field(client, app):
  with app.app_context():
    client.post(
      'ricevimento/new/?url=/',
      data={
        'data': '2020-02-01',
        'studente': 1,
        'tag': ['Let', 'Prog', 'importante', 'esame_prova']
        }
    )
    count = Tag.query.filter(Tag.nome=='esame_prova').count()
    assert count == 1
    tag = Tag.query.filter(Tag.nome=='esame_prova').all()
    count = Ricevimento.query.filter(Ricevimento.tag.contains(tag[0])).count()
    assert count == 1