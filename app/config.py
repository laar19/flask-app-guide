from sqlalchemy_utils import create_database, database_exists
from werkzeug.security import generate_password_hash
import os, datetime

def verify_boolean(var):
    if var == "false":
        return False
    return True

class Config(object):
    #SECRET_KEY = "my_secret_key" # DEBE SER 100% SECRETO, QUE NADIE TENGA ACCESO, puede ser encriptado en la base de datos
    SECRET_KEY = generate_password_hash(str(datetime.datetime.now()))
    
    # para gmail se necesita activar el acceso a aplicaciones
    # poco seguras https://myaccount.google.com/lesssecureapps
    MAIL_SERVER   = os.environ.get("MAIL_SERVER")
    MAIL_PORT     = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL  = verify_boolean(os.environ.get("MAIL_USE_SSL"))
    MAIL_USE_TLS  = verify_boolean(os.environ.get("MAIL_USE_TLS"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class DevelopmentConfig(Config):
    DEBUG                          = verify_boolean(os.environ.get("DEBUG"))
    SQLALCHEMY_DATABASE_URI        = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = verify_boolean(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS"))
    
    CHECK_DATABASE = verify_boolean(os.environ.get("CHECK_DATABASE"))
    if CHECK_DATABASE:
        if not database_exists(SQLALCHEMY_DATABASE_URI):
            create_database(SQLALCHEMY_DATABASE_URI)
