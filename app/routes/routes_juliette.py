from ..app import app, db
from .generales import *
from flask import render_template, abort
from flask import jsonify, request
from sqlalchemy import text 
from ..models.mapping import *


import requests
from flask import jsonify
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
    results = [] 
    for book in data.get("results", [])[:limit]:

        primary_location = book.get("primary_location")
        source = primary_location.get("source") if primary_location else None
        publisher = source.get("display_name") if source else ""

        result = {
            "OpenAlex_ID": book.get("id"),
            "Title": book.get("title"),
            "Publication_year": book.get("publication_year"),
            "Authors" : [author.get("author", {}).get("display_name", "") for author in book.get("authorships")],
            "Publisher" : publisher,
            "Type" : book.get("type"),
            "OpenAccess" : book.get("open_access").get("oa_status")   

        }
        results.append(result)
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

    results = [] 
    for book in data.get("results", [])[:limit]:

        primary_location = book.get("primary_location")
        source = primary_location.get("source") if primary_location else None
        publisher = source.get("display_name") if source else ""

        result = {
            "OpenAlex_ID": book.get("id"),
            "Title": book.get("title"),
            "Publication_year": book.get("publication_year"),
            "Authors" : [author.get("author").get("display_name") for author in book.get("authorships")],
            "Publisher" : publisher,
            "Type" : book.get("type"),
            "OpenAccess" : book.get("open_access").get("oa_status")   

        }
        results.append(result)

    return jsonify(results)

@app.route('/recherche/<int:page>')
def recherche(page):
    per_page = int(app.config["PER_PAGE"])
    query = request.args.get('q', '').strip()
    type_filtre = request.args.get('type', '').strip()

    # Initialiser les requêtes SQLAlchemy
    query_artists = Artists.query.filter(Artists.WikiID != None)
    query_artworks = Artworks.query

    # Appliquer la recherche textuelle si un mot-clé est donné
    if query:
        query_artists = query_artists.filter(Artists.DisplayName.ilike(f"%{query}%"))
        query_artworks = query_artworks.filter(Artworks.Title.ilike(f"%{query}%"))

    # Appliquer le filtre de type
    if type_filtre == "artistes":
        query_artworks = Artworks.query.filter(False)  # Filtre vide
    elif type_filtre == "oeuvres":
        query_artists = Artists.query.filter(False)  # Filtre vide

    # Pagination
    artists_paginated = query_artists.paginate(page=page, per_page=per_page, error_out=False)
    artworks_paginated = query_artworks.paginate(page=page, per_page=per_page, error_out=False)

    # Fusion et tri
    all_items = artists_paginated.items + artworks_paginated.items
    all_items_sorted = sorted(all_items, key=lambda x: x.DisplayName if isinstance(x, Artists) else x.Title)

    return render_template(
        "pages/recherche.html",
        items=all_items_sorted,
        artists=artists_paginated,
        artworks=artworks_paginated
    )


