from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField
class AjoutUtilisateur(FlaskForm):
    #Formulaire pour ajouter un utilisateur 
    identifiant=StringField("identifiant", validators=[])
    email=StringField("email", validators=[])
    password=PasswordField("password", validators=[])
