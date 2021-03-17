from wtforms.validators import ValidationError

class StringCheck(object):
    
    def __init__(self,message=None):
        self.message = message

    def __call__(self, form, field):
        name = field.data
        if not name.isalpha():
            message = self.message
            if message is None:
                message = field.gettext("Name must be string.")

            raise ValidationError(message)

class ResultCheck(object):

    def __init__(self, esito, message=None):
        self.esito = esito
        self.message = message

    def __call__(self, form, field):
        esito = form[self.esito]
        if (esito.data == 'respinto'):
            message = self.message
            if message is None:
                message = field.gettext("L'esito dell'esame risulta essere respinto")

            raise ValidationError(message)

