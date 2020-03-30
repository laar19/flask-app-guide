from sqlalchemy_utils import create_database, database_exists
from werkzeug.security import generate_password_hash
from app.helper import set_config
import datetime

val = None
while val == None:
    print("\nOPCIÓN INVÁLIDA\n")
    val = set_config()

class Config(object):
    #SECRET_KEY = "my_secret_key" # DEBE SER 100% SECRETO, QUE NADIE TENGA ACCESO, puede ser encriptado en la base de datos
    SECRET_KEY = generate_password_hash(str(datetime.datetime.now()))
    
    # para gmail se necesita activar el acceso a aplicaciones
    # poco seguras https://myaccount.google.com/lesssecureapps
    MAIL_SERVER   = val["MAIL_SERVER"]
    MAIL_PORT     = val["MAIL_PORT"]
    MAIL_USE_SSL  = val["MAIL_USE_SSL"]
    MAIL_USE_TLS  = val["MAIL_USE_TLS"]
    MAIL_USERNAME = val["MAIL_USERNAME"]
    MAIL_PASSWORD = val["MAIL_PASSWORD"]

class DevelopmentConfig(Config):
    DEBUG                          = val["DEBUG"]
    SQLALCHEMY_DATABASE_URI        = val["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = val["SQLALCHEMY_TRACK_MODIFICATIONS"]
    
    CHECK_DATABASE = val["CHECK_DATABASE"]
    if CHECK_DATABASE:
        if not database_exists(SQLALCHEMY_DATABASE_URI):
            create_database(SQLALCHEMY_DATABASE_URI)
