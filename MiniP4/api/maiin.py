from flask import Flask
import logging


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

from api.models import db,admin

db.app=app
db.init_app(app)
admin.init_app(app)

from api.views import *

if __name__ == '__main__':
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('log.log')
    logger.addHandler(handler)
    app.run(host='localhost', port=8000, debug=True)


