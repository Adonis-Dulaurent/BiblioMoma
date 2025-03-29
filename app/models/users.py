from datetime import datetime
from typing import Tuple, List, Optional, Union
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import and_
from ..app import app, db, login

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id : int = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pseudo : str = db.Column(db.Text, nullable=False)
    password : str = db.Column(db.String(100), nullable=False)
    email : str = db.Column(db.Text, nullable=False)

    @staticmethod
    def identification(pseudo : str, password : str, email : str) -> Optional['User']:
        """
        Identifie un utilisateur en vérifiant son pseudo et son email dans la base de données,
        puis compare le mot de passe saisi avec celui stocké.

        Args
        ----
            -Pseudo (str): Le pseudo de l'utilisateur.
            -password (str): Le mot de passe de l'utilisateur.
            -email (str): L'email de l'utilisateur 

        Returns
        --------
            Optional['User']:
                - L'utilisateur correspondant si les identifiants sont valides, sinon None
        """
        utilisateur = User.query.filter(User.pseudo == pseudo, User.email == email).first()
        if utilisateur and check_password_hash(utilisateur.password, password):
            return utilisateur
        return None

    @staticmethod
    def ajout(pseudo : str, password : str, email : str) -> Tuple[bool, List[str]]:
        """
        Ajouter un utilisateur a la base de données après validation des données

        Args:
            pseudo (str): Le pseudo de l'utilisateur
            password (str): Le mot de passe de l'utilisateur
            email (str): L'email de l'utilisateur 

        Returns
        --------
            Tuple[bool, List[str]]:
                - Si réussi, un tuple contenant un booléen indiquant que l'ajout a réussi et une liste de succès.
                - Si échec, une liste d'erreu
        """
        erreurs : List[str] = []
        if not pseudo:
            erreurs.append("Username is empty")
        if not password or len(password) < 6:
            erreurs.append("Password is empty or too short")
        if not email:
            erreurs.append("There is no email")
        
        unique = User.query.filter(
            User.pseudo == pseudo
        ).count()
        
        if unique > 0:
            erreurs.append("The nickname already exists")
        
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
        """
        Retourne l'identifiant de l'utilisateur 

        Returns:
            int: L'identifiant de l'utilisateur.
        """
        return self.id
    
@login.user_loader
def get_user_by_id(id) -> Optional[User]:
    """
    Récupération de l'utilisateur par son identifiant.

    Args
    ----
        id(int): L'identifiant de l'utilisateur 

    Returns
    -------
        Optional[User]: L'utilisateur correspondant ou None si non trouvé.
    """
    return User.query.get(int(id))


class Panier(db.Model):
    __tablename__="panier"
    id : int = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_id : int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_ajout : datetime = db.Column(db.DateTime, default=datetime.utcnow)
    bibliographie : str = db.Column(db.Text) # stocke les bibliographie generer par OpenAlex

    # Relation avec d'autre table 
    user = db.relationship('User', backref=db.backref('paniers', lazy=True))

    @staticmethod
    def ajouter_au_panier(user_id : int, bibliographie : str) -> Tuple[bool, str]:
        """
        Ajoute une nouvelle bibliographie au panier de l'utilisateur si elle n'existe pas déjà.
        Si elle existe déja, on met à jour la date d'ajout.

        Args:
            -user_id (int): identifiant de l'utilisateur.
            -bibliographie (str): Bibliographie a ajouter au panier

        Returns:
            Tuple[bool, str]:
                -Statut de l'ajout (succès ou échec) et message associé.
        """

        # Vérifier si une bibliographie identique existe déjà dans le panier de l'utilisateur
        item_existant = Panier.query.filter(Panier.user_id == user_id, Panier.bibliographie == bibliographie).first()        

        if item_existant:
            item_existant.bibliographie = bibliographie
            #si la bibiolgraphie existe déja, on met a jour la date d'ajout
            item_existant.date_ajout = datetime.utcnow()

            try: 
                db.session.commit()
                return True, "Bibliography Successfully updated"
            except Exception as erreur:
                db.session.rollback()
                return False, f"Deletion error : {str(erreur)}"
        else: 
            #Créer une novuelle entrée 
            nouvelle_biblio = Panier(
                user_id = user_id,
                bibliographie = bibliographie
            )
            try: 
                db.session.add(nouvelle_biblio)
                db.session.commit()
                return True, "Bibliography Successfully updated"
            except Exception as erreur:
                db.session.rollback
                return False, f"Deletion error : {str(erreur)}"

    @staticmethod
    def supprimer_du_panier(panier_id: int, user_id: int) -> Tuple[bool, str]:
        """
        Supprime une bibliographie du panier de l'utilisateur.

        Args
        ----
            panier_id (int): L'identifiant de la bibliographie dans la table Panier.
            user_id (int): L'identifiant de l'utilisateur 

        Returns
        -------
            Tuple[bool, str]: Statut de la suppression (succès ou échec) et message associé
        """
        item = Panier.query.filter_by(id=panier_id, user_id=user_id).first()

        if not item:
            return False, "This bibliography is not in your collection"

        try:
            db.session.delete(item)
            db.session.commit()
            return True, "Bibliography removed from your collection"
        except Exception as erreur:
            db.session.rollback() 
            return False, f"Deletion error : {str(erreur)}"