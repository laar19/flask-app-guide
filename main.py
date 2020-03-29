from flask      import Flask, make_response
from flask      import request, flash, copy_current_request_context
from flask_wtf  import CSRFProtect
from flask_mail import Mail
from sqlalchemy import exc

from app.config import DevelopmentConfig
from app.models import db, User, Comment
from app.helper import *
from app.forms  import *

import threading

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

mail = Mail()

@app.route("/")
@app.route("/index")
def index():
    if not check_login(username="username"):
        return redirect(url_for("login"))
    return render_template("index.html", title="Inicio")
    
# Crear nuevo usuario
@app.route("/signup", methods=["GET", "POST"])
def signup():
    create_form = CreateForm(request.form)

    if request.method == "POST" and create_form.validate():
        user = User(username = create_form.username.data,
                    email    = create_form.email.data,
                    password = create_form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            error_message = "El nombre de usuario ya se encuentra registrado"
            flash(error_message)
        else:
            @copy_current_request_context
            def send_message(email, username, app, mail):
                send_email(email, username, app, mail)
                
            sender = threading.Thread(name   = "mail_sender",
                                      target = send_message,
                                      args   = (user.email, user.username, app, mail))
            sender.start()

            success_message = "Usuario registrado con éxito"
            flash(success_message)
            return redirect(url_for("login"))

    return render_template("signup.html", form=create_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)

    if request.method == "POST" and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None and user.verify_password(user.password, password):
            success_message = "Bienvenido {}".format(username)
            flash(success_message)
            create_session(username, user.id)
            return redirect(url_for("index"))
        else:
            error_message = "Usuario o contraseña inválido"
            flash(error_message)

    return render_template("login.html", form=login_form)
    
# Cerrar sesión
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))

# Página para crear comentarios
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if not check_login(username="username"):
        return redirect(url_for("login"))

    comment_form = CommentForm(request.form)
    
    if request.method == "POST" and comment_form.validate():
        username = session["username"]
        user_id = session["user_id"]
        
        comment = Comment(text    = comment_form.comment.data,
                          user_id = user_id)
        
        db.session.add(comment)
        db.session.commit()
        
        success_message = "Nuevo comentario creado"
        flash(success_message)
        
    title = "Curso Flask"

    return render_template("comment.html", title=title, form=comment_form)

# Página que muestra los comentarios
@app.route("/reviews")
def reviews():
    if not check_login(username="username"):
        return redirect(url_for("login"))

    page = request.args.get("page", 1, type=int)
    per_page = 3
    # Normal order
    """
    comments = Comment.query.join(User).add_columns(
        User.username,
        Comment.id,
        Comment.text,
        Comment.create_date).order_by(Comment.create_date.desc()).paginate(page, per_page, False)
    """
    # Reverse order: .order_by(Comment.create_date.desc())
    comments = Comment.query.join(User).add_columns(
        User.username,
        Comment.id,
        Comment.text,
        Comment.create_date).order_by(Comment.create_date.desc()).paginate(page, per_page, False)
    next_url = url_for("reviews", page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for("reviews", page=comments.prev_num) \
        if comments.has_prev else None
    return render_template("reviews.html",
                            comments=comments,
                            date_format=date_format,
                            delete_comment=delete_comment,
                            id=None,
                            redirect=redirect,
                            next_url=next_url,
                            prev_url=prev_url)

# Redirecciona dependiendo si se pesionó el botón update o delete
@app.route("/update_delete", methods=["POST"])
def update_delete():
    if request.method == "POST":
        operation    = int(request.form["operation"])
        comment_text = str(request.form["comment_text"])
        id_          = int(request.form["id_"])
    
    if operation == 1:
        return redirect(url_for("update", comment_text=comment_text, id_=id_))
    elif operation == 2:
        delete_comment(Comment, db, id_, flash)
    return redirect(url_for("reviews"))

# Si se presionó el botón update redirije a la página
# con el formulario de actualización
@app.route("/update", methods=["GET", "POST"])
@app.route("/update/<string:comment_text>/<int:id_>", methods=["GET", "POST"])
def update(comment_text, id_):
    return render_template("update.html", comment_text=comment_text, id_=id_)

# Actualiza el comentario
@app.route("/update_comment", methods=["POST"])
def update_comment():
    if request.method == "POST":
        comment_text = str(request.form["comment_text"])
        id_          = int(request.form["id_"])
        comment_update(Comment, db, id_, comment_text, flash)

    return redirect(url_for("reviews"))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        db.create_all()

    app.run()
