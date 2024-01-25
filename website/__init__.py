from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from website.config import Config
from flask_mail import Mail

database = SQLAlchemy()

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    #app.run(debug=True)
    app.app_context().push()

    database.init_app(app)
    mail.init_app(app)

    # import routes from blueprints
    from website.main.routes import main
    # register blueprints
    app.register_blueprint(main)

    @app.context_processor
    def inject_theme():
        theme = session.get('theme', 'dark-theme')  # Use 'dark-theme' as the default theme
        return dict(theme=theme)

    return app


