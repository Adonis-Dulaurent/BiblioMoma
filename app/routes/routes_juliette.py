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



@app.route('/recherche/<int:page>')
def recherche(page):
    per_page = int(app.config["PER_PAGE"])
    query = request.args.get('q', '').strip()
    type_filtre = request.args.get('type', '').strip()
    movement = request.args.get('movement', '').strip()  # Filtre mouvement
    year_filter = request.args.get('year_filter', '').strip()  # Filtre par année
    artist_name = request.args.get('artist_name', '').strip()  # Filtre par artiste (pour œuvres)

    # Initialiser les requêtes SQLAlchemy
    query_artists = Artists.query.filter(Artists.WikiID != None)
    query_artworks = Artworks.query

    # Appliquer la recherche textuelle si un mot-clé est donné
    if query:
        query_artists = query_artists.filter(Artists.DisplayName.ilike(f"%{query}%"))
        query_artworks = query_artworks.filter(Artworks.Title.ilike(f"%{query}%"))

    # Appliquer le filtre par mouvement
    if movement:
        query_artists = query_artists.join(ArtistsMovements).join(Movements).filter(Movements.Label.ilike(f"%{movement}%"))

    # Appliquer le filtre par année (naissance ou décès)
    if year_filter.isdigit():  # Vérifier que c'est bien une année valide
        year_filter = int(year_filter)
        query_artists = query_artists.filter(
            (Artists.BirthDate == year_filter) | (Artists.DeathDate == year_filter)
        )

    # Appliquer le filtre d'artiste pour les œuvres
    if artist_name:
        query_artworks = query_artworks.join(Artists).filter(Artists.DisplayName.ilike(f"%{artist_name}%"))

    # Appliquer le filtre de type
    if type_filtre == "artistes":
        query_artworks = Artworks.query.filter(False)  # Désactive la recherche des œuvres
    elif type_filtre == "oeuvres":
        query_artists = Artists.query.filter(False)  # Désactive la recherche des artistes

    # Pagination
    artists_paginated = query_artists.paginate(page=page, per_page=per_page, error_out=False)
    artworks_paginated = query_artworks.paginate(page=page, per_page=per_page, error_out=False)

    # Fusion et tri des résultats
    all_items = artists_paginated.items + artworks_paginated.items
    all_items_sorted = sorted(all_items, key=lambda x: x.DisplayName if isinstance(x, Artists) else x.Title)

    return render_template(
        "pages/recherche.html",
        items=all_items_sorted,
        artists=artists_paginated,
        artworks=artworks_paginated,
        movements=Movements.query.all(),  # Pour remplir la liste déroulante des mouvements
        selected_movement=movement,
        selected_year=year_filter,
        selected_artist=artist_name  # Passer le filtre d'artiste pour préremplir le champ
    )



