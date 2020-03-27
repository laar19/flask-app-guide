from wtforms import Form, StringField, TextField
from wtforms import PasswordField, validators, HiddenField
from .models import User
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    username = StringField("Username",
        [validators.Required(message="Campo requerido"),
            validators.length(min=4, max=10, message="Ingrese un nombre de usuario válido")])

    password = PasswordField("Password",
        [validators.Required(message="Campo requerido")])

class CreateForm(Form):
    username = TextField("Username",
        [validators.Required(message="Campo requerido"),
            validators.length(min=4, max=10, message="Ingrese un nombre de usuario válido")])

    email = EmailField("Email",
        [validators.Required(message="Campo requerido"),
            validators.length(min=1, max=50, message="Ingrese un nombre de usuario válido")])

    password = PasswordField("Password",
        [validators.Required(message="Campo requerido")])
            
class CommentForm(Form):
    comment = TextField("Comentario",
        [validators.Required(message="Campo requerido"),
            validators.length(min=4, max=100, message="El campo no puede estar vacío")])
