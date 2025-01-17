from flask import Flask

from applications.extensions import db
from applications.routes.route_example import routes


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    app.register_blueprint(routes)
    return app
