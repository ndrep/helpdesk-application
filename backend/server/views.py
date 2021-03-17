from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from .models import db, Ricevimento, Studente, Tag, CdL, Esame, Insegnamento, Evento, FrequenzaCorso
from flask_admin import Admin
from wtforms import StringField
from wtforms.validators import Length, Email, DataRequired
import click
from flask.cli import with_appcontext
from .fields import AdvancedTagField
from .validator import StringCheck, ResultCheck
from .json_loader import load_db
from flask_ckeditor import CKEditorField

class StudentView(ModelView):
    column_list = ('email', 'nome', 'cognome', 'matricola', 'anno_iscrizione')
    form_excluded_columns = ('evento')
    column_searchable_list = ['email', 'nome', 'cognome', 'matricola', 'anno_iscrizione']
    form_extra_fields = {
        'email' : StringField(validators=[Email(message=u'Invalid email address')])
    }
    column_labels = {
        'email': 'Email',
        'nome': 'Nome',
        'cognome': 'Cognome',
        'matricola': 'Matricola',
        'anno_iscrizione': 'Anno iscrizione',
        'cdl': 'Corso di laurea'
    }
    form_args = {
        'nome': {
            'validators': [Length(min=2, max=20),StringCheck()]
        },
        'cognome': {
            'validators': [Length(min=2, max=20),StringCheck()]
        }
    }
    page_size = 30

class CdLView(ModelView):
    column_list = ('codice', 'nome', 'tipo')
    form_columns = ('codice', 'nome', 'tipo')   
    column_searchable_list = ['nome', 'tipo']
    page_size = 30

class EventoView(ModelView):
    form_excluded_columns = ('type')  

class RicevimentoView(ModelView):
    form_excluded_columns = ('type')
    form_overrides = dict(domande=CKEditorField,suggerimenti=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'
    form_extra_fields = {
        'tag' : AdvancedTagField()
    }
    form_args = {
    'studente': {
        'validators': [DataRequired("Dev'essere inserito uno studente")]
    }
}
    
    page_size = 30
        
class TagView(ModelView):
    column_list = ('nome','ricevimento')
    form_excluded_columns = ['ricevimento']
    column_searchable_list = ['nome']
    page_size = 30

class EsameView(ModelView):
    column_list = ('data', 'tipo_esame', 'esito', 'voto', 'accettato')
    form_excluded_columns = ('type')
    form_args = {
        'voto': {
            'validators': [ResultCheck('esito')]
        },
        'accettato': {
            'validators': [ResultCheck('esito')]
        },
        'studente': {
            'validators': [DataRequired("Dev'essere inserito uno studente")]
        }
    }

class FrequenzaCorsoView(ModelView):
    form_excluded_columns = ('type')

class InsegnamentoView(ModelView):
    column_list = ('nome', 'crediti', 'laboratorio', 'scritto', 'orale', 'progetto')
    form_excluded_columns = ('esame')

def init_admin(app):
    admin = Admin(
        app,
        template_mode = 'bootstrap3',
        index_view=StudentView(Studente, db.session, url='/', endpoint='admin')
        )
    admin.add_views(FrequenzaCorsoView(FrequenzaCorso, db.session),InsegnamentoView(Insegnamento, db.session), CdLView(CdL, db.session), EsameView(Esame, db.session), RicevimentoView(Ricevimento, db.session))
    admin.add_link(MenuLink(name='Back to App', url='/'))
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    db.drop_all()
    db.create_all()
    load_db('server/data.json')
    click.echo('Initialized the database.')