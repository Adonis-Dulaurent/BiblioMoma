from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField
class AjoutUtilisateur(FlaskForm):
    #Formulaire pour ajouter un utilisateur 
    identifiant=StringField("prenom", validators=[])
    password=PasswordField("password", validators=[])

class Connexion(FlaskForm):
    prenom = StringField("prenom", validators=[])
    password = PasswordField("password", validators=[])