import os
from website import settings

class Config:

    SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI

    SECRET_KEY = settings.SECRET_KEY
    
    MAIL_SERVER = settings.MAIL_SERVER
    MAIL_PORT = settings.MAIL_PORT
    MAIL_USE_TLS = settings.MAIL_USE_TLS
    MAIL_USERNAME = settings.MAIL_USERNAME
    MAIL_PASSWORD = settings.MAIL_PASSWORD