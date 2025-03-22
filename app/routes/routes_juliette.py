from ..app import app, db
from .generales import *
from flask import render_template, abort
from flask import jsonify
from sqlalchemy import text 
from ..models.mapping import *


import requests
from flask import jsonify
from flask import jsonify

@app.route('/oeuvres/<int:id_oeuvre>/bibliography')
def get_oeuvre_biblio(id_oeuvre):
    """Renvoie la bibliographie en JSON via OpenAlex."""

    oeuvre = Artworks.query.filter(Artworks.id == id_oeuvre).first()
    if not oeuvre:
        return jsonify({"error": "L'œuvre n'est pas référencée au MoMA"}), 404

    query_title = oeuvre.Title.replace(" ", "+")
    base_url = f"https://api.openalex.org/works?page=1&filter=primary_topic.field.id:fields/12,default.search:{query_title}&sort=relevance_score:desc&per_page=10"

    response = requests.get(base_url)
    if response.status_code != 200:
        return jsonify({"error": "Il n'y a pas de bibliographie directement associée à cette oeuvre."}), 500

    data = response.json()
    results = [{
        "OpenAlex_ID": book.get("id"),
        "Title": book.get("title"),
        "Publication_year": book.get("publication_year")
    } for book in data.get("results", [])[:10]]

    return jsonify(results)





@app.route('/artistes/<id_artist>/bibliography')
def get_artist_biblio(id_artist):
    """Renvoie la bibliographie en JSON via OpenAlex."""

    artiste = Artists.query.filter(Artists.WikiID == id_artist).first()
    if not artiste:
        return jsonify({"error": "L'artiste n'est pas référencée au MoMA"}), 404

    query_title = artiste.DisplayName.replace(" ", "+")
    base_url = f"https://api.openalex.org/works?page=1&filter=primary_topic.field.id:fields/12,default.search:{query_title}&sort=relevance_score:desc&per_page=10"

    response = requests.get(base_url)
    if response.status_code != 200:
        return jsonify({"error": "Il n'y a pas de bibliographie directement associée à cet artiste."}), 500

    data = response.json()
    results = [{
        "OpenAlex_ID": book.get("id"),
        "Title": book.get("title"),
        "Publication_year": book.get("publication_year")
    } for book in data.get("results", [])[:10]]

    return jsonify(results)
