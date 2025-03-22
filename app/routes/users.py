from flask import url_for, render_template, redirect, request, flash
from flask_login import login_user, current_user, logout_user
from ..models.users import User, Panier
from ..models.formulaires import AjoutUtilisateur, Connexion
from ..utils.transformations import clean_arg
from ..app import app, db, login

@app.route("/utilisateurs/ajout", methods=["GET", "POST"])
def ajout_utilisateur():

    form =AjoutUtilisateur()

    if form.validate_on_submit():
        statut, donnees = User.ajout(
            pseudo=clean_arg(request.form.get("pseudo", None)),
            password=clean_arg(request.form.get("password", None)),
            email=clean_arg(request.form.get("email", None))
        )

        if statut is True: 
            flash("Ajout effectué", "success")
            return redirect(url_for("index"))
        else:
            flash(",".join(donnees), "error")
            return render_template("pages/ajout_utilisateur.html", form=form)
    else:
        return render_template("pages/ajout_utilisateur.html", form=form)

@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def connexion():
    form = Connexion()

    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté", "info")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        utilisateur = User.identification(
            pseudo=clean_arg(request.form.get("pseudo", None)),
            password=clean_arg(request.form.get("password", None)),
            email=clean_arg(request.form.get("email", None))
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("guide"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
            return render_template("pages/connexion.html", form=form)

    else:
        return render_template("pages/connexion.html", form=form)

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("vous êtes déconnecté", "info")
    return redirect(url_for("guide"))

login.login_view = 'connexion'

@app.route("/utilisateurs/panier")
def afficher_panier():  
    """
    afficher le panier de l'utilisateur 
    """
    #verification si l'utilisateur est connecté 
    if not current_user.is_authenticated:
        flash("You must be logged in to access your basket")
        return redirect(url_for("connexion", next=request.path))
        
    panier = Panier.obtenir_panier_utilisateur(current_user.id)
    return render_template('pages/panier.html', panier=panier)
