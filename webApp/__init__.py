import os

from flask import Flask


def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'iHG4U7L7XY5e3bfN92B6NqplKI6wSRIf',
        DATABASE = os.path.join(app.instance_path, 'webApp.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import items
    app.register_blueprint(items.bp)

    from . import cashregister
    app.register_blueprint(cashregister.bp)
    app.add_url_rule('/', endpoint='index')

    return app
