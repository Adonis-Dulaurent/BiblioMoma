from ..app import app, db
from flask import render_template, abort
from flask import jsonify, request
from sqlalchemy import text 
from ..models.mapping import *


import requests
from flask import jsonify

@app.route('/oeuvres/<id_oeuvre>/bibliography')
def get_oeuvre_biblio(id_oeuvre):
    """Renvoie la bibliographie en JSON via OpenAlex."""

    oeuvre = Artworks.query.filter(Artworks.id == id_oeuvre).first()
    if not oeuvre:
        return jsonify({"error": "L'œuvre n'est pas référencée"}), 404

    query_title = oeuvre.Title.replace(" ", "+")
    limit = request.args.get("limit", default=10, type=int)  


    base_url = f"https://api.openalex.org/works?page=1&filter=primary_topic.field.id:fields/12,default.search:{query_title}&sort=relevance_score:desc&per_page={limit}"

    response = requests.get(base_url)
    if response.status_code != 200 or response.text == "":
        return jsonify({"error": "No result on OpenAlex for this artwork."}), 500

    data = response.json()
    results = [{
        "OpenAlex_ID": book.get("id"),
        "Title": book.get("title"),
        "Publication_year": book.get("publication_year")
    } for book in data.get("results", [])[:limit]]
    return jsonify(results)

    # user = int(input("combien voulez vous de livre"))
    # option_1 = results[0:user]



@app.route('/artistes/<id_artist>/bibliography')
def get_artiste_biblio(id_artist):
    """Récupère la bibliographie associée à un artiste via OpenAlex."""
    artist = Artists.query.filter(Artists.WikiID == id_artist).first()
    if not artist:
        return jsonify({"error": "No reference for this artist in the database"}), 404

    query_title = artist.DisplayName.replace(" ", "+")
    limit = request.args.get("limit", default=10, type=int)  


    base_url = f"https://api.openalex.org/works?page=1&filter=primary_topic.field.id:fields/12,default.search:{query_title}&sort=relevance_score:desc&per_page={limit}"

    response = requests.get(base_url)
    if response.status_code != 200 or response.text == "":
        return jsonify({"error": "No result on OpenAlex for this artist."}), 500

    data = response.json()
    results = [{
        "OpenAlex_ID": book.get("id"),
        "Title": book.get("title"),
        "Publication_year": book.get("publication_year")
    } for book in data.get("results", [])[:limit]]

    return jsonify(results)
