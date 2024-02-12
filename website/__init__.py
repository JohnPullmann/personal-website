from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from website.config import Config
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

database = SQLAlchemy()

mail = Mail()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    #app.run(debug=True)

    database.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # import routes from blueprints
    from website.main.routes import main
    from website.users.routes import users
    # register blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)

    @app.context_processor
    def inject_theme():
        theme = session.get('theme', 'dark-theme')  # Use 'dark-theme' as the default theme
        return dict(theme=theme)

    return app


