from ..app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pseudo = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Text, nullable=False)
    
    @staticmethod
    def ajout(pseudo, password, email):
        erreurs = []
        if not pseudo:
            erreurs.append("le pseudo est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")
        if not email:
            erreurs.append("Il n'y a pas d'email")
        
        unique = User.query.filter(
            User.pseudo == pseudo
        ).count()
        
        if unique > 0:
            erreurs.append("Le pseudo existe déja")
        
        if len(erreurs) > 0:
            return False, erreurs
        
        utilisateur = User(
            pseudo=pseudo,
            password=generate_password_hash(password),
            email=email
        )
        
        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]
    
    def get_id(self):
        return self.id
    
@login.user_loader
def get_user_by_id(id):
    return User.query.get(int(id))

@staticmethod
def identification(pseudo, password):
    utilisateur = User.query.filter(User.pseudo == pseudo).first()
    if utilisateur and check_password_hash(utilisateur.password, password):
        return utilisateur
    return None