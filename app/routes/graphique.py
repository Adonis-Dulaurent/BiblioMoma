from collections import Counter
from flask import render_template, jsonify
from flask_login import login_required, current_user
from app.models.users import Panier
from ..app import app, db, login

@app.route("/graphique_open_access", methods=["GET"])
@login_required
def afficher_graphique_open_access():
    user_id = current_user.id
    bibliographies = Panier.query.filter_by(user_id=user_id).all()

    categories = ["diamond", "gold", "green", "hybrid", "bronze", "closed"]
    open_access_counts = Counter(biblio.open_access for biblio in bibliographies if biblio.open_access in categories)

    data = {category: open_access_counts.get(category, 0) for category in categories}

    return jsonify(data) 


@app.route("/graphique_types", methods=["GET"])
@login_required
def afficher_graphique_types():
    user_id = current_user.id
    bibiolgraphies = Panier.query.filter_by(user_id=user_id).all()

    types = ["book-section", "monograph","report-component", "report", "peer-review", "book-track",
     "journal-article","book-part","other", "book", "journal-volume", "book-set", "reference-entry", "proceedings-article",
     "journal", "component","book-chapter","proceedings-series", "report-series", "proceedings", "database",
     "standard", "reference-book", "posted-content", "journal-issue", "dissertation", "grant", "dataset", "book-series",
     "edited-book"]

    type_counts = Counter(biblio.type for biblio in bibiolgraphies if biblio.type in types)

    data = {type_: type_counts.get(type_, 0) for type_ in types}

    return jsonify(data) 