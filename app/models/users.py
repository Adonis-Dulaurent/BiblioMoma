from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from ..app import app, db

class Users(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer, unique=True, nullable=False,primary_key=True, autoincrement=True)
    identifiant=db.Column(db.Text, nullable=False)
    password=db.Column(db.String(100), nullable=False)
    email=db.Column(db.Text, nullable=False)

    @staticmethod
    def ajout(identifiant,password, email):
        erreurs=[]
        "Gestion des erreurs si password vide, ou trop court et l'identifiant vide"
        if not identifiant:
            erreurs.append("l'identifiant est vide")
        if not password: 
            erreurs.append("le password est vide ou trop court")
        if len(password)<6:
            erreurs.append("le mot de passe est trop court")

        unique = Users.query.filter(
            db.or_(Users.identifiant == identifiant, Users.email == email)).count()
        if unique > 0: 
            erreurs.append("L'identifiant ou l'email existe déja")

        if len(erreurs)>0:
            return False, erreurs

        utilisateur = Users(
            identifiant=identifiant,
            email=email,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]
