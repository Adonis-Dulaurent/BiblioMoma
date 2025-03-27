from flask import url_for, render_template, redirect, request, flash, send_file
from flask_login import login_user, current_user, logout_user, login_required
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
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
            return redirect(url_for("guide"))
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
        return redirect(url_for("guide"))

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
@login_required
def afficher_panier(): 
   
    """
    afficher le panier de l'utilisateur 
    """
    #verification si l'utilisateur est connecté
    user_id = current_user.id 
    if not user_id:
        flash("You must be logged in to access your basket")
        return redirect(url_for("connexion", next=request.path))

    bibliographies = Panier.query.filter_by(user_id=user_id).all()
    return render_template('pages/panier.html', bibliographies=bibliographies)

@app.route("/ajouter_au_panier", methods=["POST"])
@login_required
def ajouter_au_panier():
    """
    Permet d'ajouter une bibliographie à l'utilistateur connecté
    """
    user_id = current_user.id 
    bibliographie = request.form.get("bibliography")

    if not bibliographie: 
        flash("Aucune bibliographie sélectionné.", "danger")
        return redirect(request.referrer)

    success, message = Panier.ajouter_au_panier(user_id, bibliographie)

    if success: 
        flash("Bibliographie ajouté avec succès !", "succès")
    else : 
        flash(f"Erreur : {message}", "danger")

    return redirect(request.referrer)

@app.route("/supprimer_du_panier/<int:panier_id>")
@login_required
def supprimer_du_panier(panier_id):
    
    success, message = Panier.supprimer_du_panier(panier_id, current_user.id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    return redirect(url_for('afficher_panier'))

@app.route("/exporter_bibliographies", methods=["POST"])
@login_required
def exporter_bibliographies():
    """
    Exporter toutes les bibligraphies de l'utilisateur connecté au format pdf
    """

    user_id = current_user.id
    bibliographies = Panier.query.filter_by(user_id=user_id).all()

    if not bibliographies:
        flash("No bibliography to export", "warning")
        return redirect(request.referrer) 

    # Création d'un buffer en mémoire pour le pdf
    buffer = io.BytesIO()

    #Créer le document pdf 
    doc = SimpleDocTemplate(buffer, pagesizes=letter)
    styles = getSampleStyleSheet()

    # liste pour stocker les éléments pdf 
    story = []
    
    #Titre du document 
    title = Paragraph("My Bibliography", styles['Title'])
    story.append(title)
    story.append(Spacer(1,12))

    #Ajouter a chaque bibliographie
    for biblio in bibliographies:

        #Date d'ajout : 
        biblio_date = Paragraph(f"Ajouté le : {biblio.date_ajout.strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
        story.append(biblio_date)

        #contenu bibliographie
        biblio_content =Paragraph(biblio.bibliographie, styles['Normal'])
        story.append(biblio_content)

        # Espacement entre les items
        story.append(Spacer(1,12))

    #Génération de la biblio 
    doc.build(story)

    buffer.seek(0)

    #téléchargement 
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True, 
        download_name='ma_bibliotheque.pdf'
    )
