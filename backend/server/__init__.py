import os
from flask import Flask
from flask_ckeditor import CKEditor
from .views import init_admin
from .api import api
from pathlib import Path

def create_app(test_config=None):
    app = Flask(__name__)
    ckeditor = CKEditor(app)
    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=''.join(['sqlite:////', os.path.join(app.instance_path, 'datab.db')]),
        SECRET_KEY='dev',
    )

    from .models import db
    db.init_app(app)

    with app.app_context():
        init_admin(app)
        
    Path(app.instance_path).mkdir(exist_ok = True)
    app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
    app.register_blueprint(api, url_prefix="/api")

    return app