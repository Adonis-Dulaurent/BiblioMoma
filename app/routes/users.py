from flask import url_for, render_template, redirect, request, flash
from ..models.users import Users
from ..models.formulaire import AjoutUtilisateur
from ..utils.transformation import clean_arg
from .. app import app,db

@app.route("/utilisateurs/ajout", methods=["GETS", "POST"])
def ajout_utilisateurs():
    form = ajout_utilisateurs()

    if form.validate_on_submit():
        statut, donnees = Users.ajout(
            identifiant=clean_arg(request.form.get("identifiant", NONE)),
            email=clean_arg(request.form.get("email", NONE)),
            password=clean_arg(request.form.get("password", NONE))
        )
        if statut is True: 
            flash("Ajout effectué," "success")
            return redirect(url_for("acceuil"))
        else: 
            flash(",".join(donnees), "error")
            return render_template ("pages/ajout_utilisateur.html", form=form)
    else: 
        return render_template("pages/ajout_utilisateur.html", form=form)

