from wtforms import widgets
from flask_admin.form import Select2TagsField
from .models import db, Tag

class AdvancedTagWidget(widgets.Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-tags', '1')


        allow_blank = getattr(field, 'allow_blank', False)

        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(AdvancedTagWidget, self).__call__(field, **kwargs)


class AdvancedTagField(Select2TagsField):

    widget = AdvancedTagWidget(multiple=True)

    def pre_validate(self, form):
        pass
    
    def process_formdata(self, valuelist):

        if valuelist:
            self.data = []
            for tagname in valuelist:
                rv = Tag.query.filter_by(nome=tagname).first()
                if rv:
                    self.data.append(rv)
                else:
                    tag = Tag(nome=tagname)
                    db.session.add(tag)
                    db.session.commit()
                    self.data.append(tag)
        else:
            self.data = []

    def iter_choices(self):

        self.blank_text = ""

        tags = list(set([str(tag.nome) for tag in Tag.query.all()]))

        self.choices = [[tag, tag] for tag in tags]

        for value, label in self.choices:
            yield (value, label, False)
