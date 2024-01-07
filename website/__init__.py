from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.config import Config

database = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    #app.run(debug=True)
    app.app_context().push()

    database.init_app(app)

    # import routes from blueprints
    from website.main.routes import main
    # register blueprints
    app.register_blueprint(main)

    return app


