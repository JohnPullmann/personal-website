import os

basedir = os.path.abspath(os.path.dirname(__file__))

# All secrets come from the environment; nothing secret belongs in this file.
# Production values live in /opt/johnpullmann/app.env on the server.
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'site.db'))

SECRET_KEY = os.environ.get('SECRET_KEY')

MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('EMAIL_USER')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
