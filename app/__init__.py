from contextlib import contextmanager

from flask import Flask, g

from .db import create_tables, get_session, init_db
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    init_db(app.config["SQLALCHEMY_DATABASE_URL"])
    create_tables()
    app.register_blueprint(bp)

    @app.before_request
    def before_request():
        g.session = get_session()

    @app.teardown_appcontext
    def teardown_session(exception=None):
        if hasattr(g, "session"):
            g.session.close()

    return app
