from datetime import datetime
from typing import Tuple, List, Optional, Union
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..app import app, db, login

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id : int = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pseudo : str = db.Column(db.Text, nullable=False)
    password : str = db.Column(db.String(100), nullable=False)
    email : str = db.Column(db.Text, nullable=False)

    @staticmethod
    def identification(pseudo : str, password : str, email : str) -> Optional['User']:
        """_summary_

        Returns:
            _type_: _description_
        """
        utilisateur = User.query.filter(User.pseudo == pseudo, User.email == email).first()
        if utilisateur and check_password_hash(utilisateur.password, password):
            return utilisateur
        return None

    @staticmethod
    def ajout(pseudo : str, password : str, email : str):
        """_summary_

        Args:
            pseudo (str): _description_
            password (str): _description_
            email (str): _description_

        Returns:
            _type_: _description_
        """
        erreurs : List[str] = []
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
    
    
    def get_id(self) -> int:
        return self.id
    
@login.user_loader
def get_user_by_id(id) -> int:
    return User.query.get(int(id))

"""
@staticmethod
def identification(pseudo, password, email):
    utilisateur = User.query.filter(User.pseudo == pseudo, User.email == email).first()
    if utilisateur and check_password_hash(utilisateur.password, password):
        return utilisateur
    return None
"""

class Panier(db.Model):
    __tablename__="panier"
    id : int  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id : int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_ajout : datetime = db.Column(db.DateTime, default=datetime.utcnow)
    bibliographie : str = db.Column(db.Text) # stocke les bibliographie generer par OpenAlex

    # Relation avec d'autre table 
    user = db.relationship('User', backref=db.backref('paniers', lazy=True))

    @staticmethod
    def ajouter_au_panier(user_id : int, bibliographie : str) -> Tuple[bool, str]:
        """
        Ajoute une nouvelle bibliographie au panier de l'utilisateur si elle n'existe pas déjà

        Args:
            user_id (int): _description_
            bibliographie (str): _description_

        Returns:
            Tuple[bool, str]: _description_
        """
        # Vérifier si une bibliographie identique existe déjà dans le panier de l'utilisateur
        item_existant = Panier.query.filter_by(user_id==user_id, bibliographie==bibliographie).first()
        
        if item_existant:
            item_existant.bibliographie = bibliographie
            item_existant.date_ajout = datetime.utcnow()

            try: 
                db.session.commit()
                return True, "Bibliographie Mise à jour avec succès"
            except Exception as erreur:
                return False, str(erreur)
        else: 
            #Créer une novuelle entrée 
            nouvelle_biblio = Panier(
                user_id = user_id,
                bibliographie = bibliographie
            )
            try: 
                db.session.add(nouvelle_biblio)
                db.session.commit()
                return True, "Bibliographie ajoutée avec succès"
            except Exception as erreur:
                return False, str(erreur)

    @staticmethod
    def supprimer_bibliographie(biblio_id : int, user_id : int) -> Tuple[bool, str]:
        """_summary_

        Args:
            biblio_id (int): _description_
            user_id (int): _description_

        Returns:
            Tuple[bool, str]: _description_
        """
        item = Panier.query.filter_by(id==biblio_id, user_id==user_id)

        if not item: 
            return False, "Cette bibliographie n'est pas dans votre collection"

        try: 
            db.session.delete(item)
            db.session.commit()
            return True, "Bibliographie retiré de votre collection"
        except Exception as erreur: 
            return False, str(erreur)
    
    @staticmethod
    def obtenir_panier_utilisateur(user_id : int) -> List['Panier']:
        return Panier.query.filter_by(user_id=user_id).all()
