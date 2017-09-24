from flask import Flask
import logging
from flask_cors import CORS

api = Flask(__name__, static_url_path='/static')

CORS(api)
errorhandler = api.errorhandler
log = api.logger
# logging.getLogger('flask_cors').level = logging.DEBUG

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

api.config.from_object('config')
# db = SQLAlchemy(api)


from app import views  # noqa
