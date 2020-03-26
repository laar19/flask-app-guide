from sqlalchemy_utils import create_database, database_exists
from werkzeug.security import generate_password_hash
import os, json, datetime

with open("app/config.json") as f:
    conf = json.load(f)

class Config(object):
    #SECRET_KEY = "my_secret_key" # DEBE SER 100% SECRETO, QUE NADIE TENGA ACCESO, puede ser encriptado en la base de datos
    SECRET_KEY = generate_password_hash(str(datetime.datetime.now()))
    
    # para gmail se necesita activar el acceso a aplicaciones
    # poco seguras https://myaccount.google.com/lesssecureapps
    MAIL_SERVER   = conf["Config"]["MAIL_SERVER"]
    MAIL_PORT     = conf["Config"]["MAIL_PORT"]
    MAIL_USE_SSL  = conf["Config"]["MAIL_USE_SSL"]
    MAIL_USE_TLS  = conf["Config"]["MAIL_USE_TLS"]
    MAIL_USERNAME = conf["Config"]["MAIL_USERNAME"]
    #MAIL_PASSWORD = os.environ.get("PASSWORD_EMAIL_CF")
    MAIL_PASSWORD = conf["Config"]["MAIL_PASSWORD"] # ES MEJOR HACERLO CON VARIABLES DE ENTORNO

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = conf["DevelopmentConfig"]["SQLALCHEMY_DATABASE_URI"]
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/curso_flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = conf["DevelopmentConfig"]["SQLALCHEMY_TRACK_MODIFICATIONS"]

    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)