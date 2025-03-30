from typing import Dict, List, Optional, Union
from collections import Counter
from flask import render_template, jsonify, Response
from flask_login import login_required, current_user
from app.models.users import Panier
from ..app import app, db, login

@app.route("/graphique_open_access", methods=["GET"])
@login_required
def afficher_graphique_open_access() -> Response :
    """
    Generer les données pour un graphique montrant la repartition des livres en open sources
    dans la bibligoraphie de l'utilisateur connecté.
    
    Returns 
    -------
    Response : Un objet JSON contenant la repartition des livres en open source.

    """
    user_id : int = current_user.id
    bibliographies : List[Panier] = Panier.query.filter_by(user_id=user_id).all()

    categories : list [str]= ["diamond", "gold", "green", "hybrid", "bronze", "closed"]
    open_access_counts : Counter = Counter(biblio.open_access for biblio in bibliographies if biblio.open_access in categories)

    data : Dict[str, int] = {category: open_access_counts.get(category, 0) for category in categories}

    return jsonify(data) 


@app.route("/graphique_types", methods=["GET"])
@login_required
def afficher_graphique_types() -> Response:
    """
    Generer les donnes bibliographique montrant la repartition des types de documents 
    dans la bibliographie de l'utilisateur.

    returns
    -------
    Response : Un objet JSON contenant le nombre de publications par type de document.
    """

    user_id : int = current_user.id
    bibiolgraphies : List [Panier] = Panier.query.filter_by(user_id=user_id).all()

    types : Dict [str] = ["book-section", "monograph","report-component", "report", "peer-review", "book-track",
     "journal-article","book-part","other", "book", "journal-volume", "book-set", "reference-entry", "proceedings-article",
     "journal", "component","book-chapter","proceedings-series", "report-series", "proceedings", "database",
     "standard", "reference-book", "posted-content", "journal-issue", "dissertation", "grant", "dataset", "book-series",
     "edited-book"]

    type_counts : Counter = Counter(biblio.type for biblio in bibiolgraphies if biblio.type in types)

    data : Dict[str, int] = {type_: type_counts.get(type_, 0) for type_ in types}

    return jsonify(data) 