from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField

class AjoutUtilisateur(FlaskForm):
    #Formulaire pour ajouter un utilisateur 
    pseudo=StringField("pseudo", validators=[])
    password=PasswordField("password", validators=[])
    email=StringField("email", validators=[])

class Connexion(FlaskForm):
    pseudo=StringField("pseudo", validators=[])         
    password = PasswordField("password", validators=[])
    email = StringField("email", validators=[])