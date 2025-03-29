from typing import Union, Optional
from collections import Counter
from flask import url_for, render_template, redirect, request, flash, send_file, Response
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
def ajout_utilisateur() -> Union[str,Response]:
    """
    Route permettant d'ajouter l'utilisateur avec validation du formulaire

    Returns
    -------
        Union[str,Response]: 
        - Redirection vers la page 'guide' si l'ajout est réussi.
        - Recharge de la page du formulaire avec un message `error` en cas d'erreur.
    """

    form =AjoutUtilisateur()

    if form.validate_on_submit():
        statut, donnees = User.ajout(
            pseudo=clean_arg(request.form.get("pseudo", None)),
            password=clean_arg(request.form.get("password", None)),
            email=clean_arg(request.form.get("email", None))
        )

        if statut is True: 

            flash("User added", "success")

            return redirect(url_for("guide"))
        else:
            flash(",".join(donnees), "danger")
            return render_template("pages/ajout_utilisateur.html", form=form)
    else:
        return render_template("pages/ajout_utilisateur.html", form=form)

@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def connexion() -> Union[str, Response]:
    """
    Route permettant a l'utilisateur de se connecter 

    Returns
    -------
        Union[str, Response]
        - Redirection vers la page 'guide' avec un message, si l'utilisateur est déja connecté.
        - Redirection vers la page 'guide' avec un message, si la connexion est réussie.
        - Recharge de la page du formulaire avec un message `error` en cas d'erreur.

    """
    form = Connexion()

    if current_user.is_authenticated is True:

        flash("You're already logged in", "info")

        return redirect(url_for("guide"))

    if form.validate_on_submit():
        utilisateur = User.identification(
            pseudo=clean_arg(request.form.get("pseudo", None)),
            password=clean_arg(request.form.get("password", None)),
            email=clean_arg(request.form.get("email", None))
        )
        if utilisateur:

            flash("Logged in!", "success")
            login_user(utilisateur)
            return redirect(url_for("guide"))
        else:
            flash("Unknown identifiers", "error")

            return render_template("pages/connexion.html", form=form)

    else:
        return render_template("pages/connexion.html", form=form)

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion() -> Response:
    """
    Route qui déconnecte l'utilisateur, s'il est authentifié, puis redirige sur 'guide'. 

    Returns
    -------
        Response
        - Redirection vers la page 'guide' avec un message flash 
    """
    if current_user.is_authenticated is True:
        logout_user()

    flash("Logged out", "info")

    return redirect(url_for("guide"))

#Défintion de la page de connexion par défaut avec flah login
login.login_view = 'connexion'

@app.route("/utilisateurs/panier")
@login_required
def afficher_panier() -> Union[str, Response]: 
    """
    Affiche le panier de l'utilisateur connecté.

    Returns
    -------
        Union[str, Response]
        - Si l'utilisateur n'est pas connecté, redirection vers la page 'connexion' avec message fash 
        - su l'utilisateur est connecté redirection vers la page 'panier.html'
    """
    #verification si l'utilisateur est connecté
    user_id : int = current_user.id 
    if not user_id:
        flash("You must be logged in to access your basket")
        return redirect(url_for("connexion", next=request.path))

    bibliographies : list[Panier] = Panier.query.filter_by(user_id=user_id).all()
    return render_template('pages/panier.html', bibliographies=bibliographies)

@app.route("/ajouter_au_panier", methods=["POST"])
@login_required
def ajouter_au_panier() -> Response:

    """
    Ajoute une ou plusieurs bibliographies au panier de l'utilisateur connecté.

    Returns
    -------
    Response
        - Si aucune bibliographie n'est sélectionnée, redirige vers la page précédente avec un message d'erreur.
        - Si une ou plusieurs bibliographies sont sélectionnées, elles sont ajoutées à la base de données (table Panier),
          puis redirection avec un message de succès ou d'erreur selon les cas.
    """


    user_id : int = current_user.id 
    bibliographies : list[str] = request.form.getlist("bibliography[]")
    authors : list[str] = request.form.getlist("authors[]")
    types : list[str] = request.form.getlist("type[]")
    open_access : list[str] = request.form.getlist("open_access[]")
    date_parution : list[int] = request.form.getlist("date_parution[]")
    publisher : list [str] = request.form.getlist("publisher[]")

    if not bibliographies: 

        flash("No bibliography selected.", "danger")
        return redirect(request.referrer)

    for bibliographie, author, type, access, date_parution, publisher in zip(bibliographies, authors, types, open_access, date_parution, publisher):
        success, message = Panier.ajouter_au_panier(user_id, bibliographie, author, type, access, date_parution, publisher)

    if success: 

        flash("Bibliography added successfully!", "succès")

    else : 
        flash(f"Erreur : {message}", "danger")

    return redirect(request.referrer)

@app.route("/supprimer_du_panier/<int:panier_id>")
@login_required
def supprimer_du_panier(panier_id: int) -> Response:
    """
    Permet de supprimer une bibliographie du panier

    Args:
        panier_id (int): Identifiant de la bibliographie dans le panier

    Returns:
        Response: Redirection vers la page 'afficher_panier' avec un message flash
    """
    success, message = Panier.supprimer_du_panier(panier_id, current_user.id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('afficher_panier'))


@app.route("/exporter_bibliographies", methods=["POST"])
@login_required
def exporter_bibliographies() -> Response:
    """ 
    Exporter toutes les bibliographies de l'utilisateur connecté au format PDF.

    Returns
    -------
        Response: 
        - Si aucune bibliographie à exporter, redirection avec un message 'danger'
        - Si bibliographies à exporter, téléchargement d'un document PDF.
    """

    user_id: int = current_user.id
    bibliographies = Panier.query.filter_by(user_id=user_id).all()

    if not bibliographies:
        flash("No bibliography to export", "danger")
        return redirect(request.referrer) 

    # Création d'un buffer en mémoire pour le pdf
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Liste pour stocker les éléments du PDF
    story = []

    # Titre du document
    title = Paragraph("My Bibliography", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Ajout des bibliographies avec auteur et année
    for biblio in bibliographies:
        authors = biblio.authors if hasattr(biblio, 'authors') else "Anonymous"
        annee = str(biblio.date_parution) if hasattr(biblio, 'date_parution') and biblio.date_parution else "n.d"
        publisher = biblio.publisher.strip() if hasattr(biblio, 'publisher') and biblio.publisher and biblio.publisher.strip() else "n.p"


        # Création du texte final
        biblio_content = Paragraph(f"{authors} ({annee}). <i>{biblio.bibliographie}</i>. {publisher} ", styles['Normal'])
        story.append(biblio_content)
        story.append(Spacer(1, 12)) 

    # Génération du PDF
    doc.build(story)

    buffer.seek(0)

    # Téléchargement du fichier PDF
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True, 
        download_name='ma_bibliotheque.pdf'
    )
