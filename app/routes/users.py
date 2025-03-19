from flask import url_for, render_template, redirect, request, flash
from flask_login import login_user, current_user
from ..models.users import User
from ..models.formulaires import AjoutUtilisateur
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
            return redirect(url_for("acceuil"))
        else:
            flash(",".join(donnees), "error")
            return render_template("pages/ajout_utilisateur.html", form=form)
    else:
        return render_template("pages/ajout_utilisateur.html", form=form)

@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def connexion():
    form = connexion()

    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté", "info")
        return redirect(url_for("accueil"))

    if form.validate_on_submit():
        utilisateur = User.identification(
            prenom=clean_arg(request.form.get("prenom", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("accueil"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
            return render_template("pages/connexion.html", form=form)

    else:
        return render_template("pages/connexion.html", form=form)

login.login_view = 'connexion'