from flask      import session, render_template, redirect, url_for
from flask_mail import Message

def date_format(date):
    months = ["Enero", "Febrero", "Marzo", "Abril",
             "Mayo", "Junio", "Julio", "Agosto",
             "Septiembe", "Octubre", "Noviembre", "Diciembre"]
             
    month = months[date.month - 1]
    
    return "{} de {} del {}".format(date.day, month, date.year)

def check_login(username):
    if "username" in session:
        username = session["username"]
        return True
    return False

def create_session(username, user_id):
    session["username"] = username
    session["user_id"]  = user_id
    
def send_email(user_email, username):
    msg = Message("REGISTRO EXITOSO",
        sender     = app.config["MAIL_USERNAME"],
        recipients = [user_email])
    msg.html = render_template("email.html", username=username)
    mail.send(msg)