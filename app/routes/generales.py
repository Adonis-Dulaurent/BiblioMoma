import os

from flask import render_template, jsonify, request
from sqlalchemy import text 

from ..models.mapping import *
from ..app import app, db



@app.route('/')
@app.route('/home')
def accueil():
    image_folder = os.path.join(app.static_folder, "images")
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg", ".gif"))]
    
    print("Images found:", images)  # Debugging line
    
    return render_template("pages/index.html", images=images)

@app.route('/cent_oeuvres_artistes')
def cent_oeuvres_artistes():
    return render_template("pages/100_oeuvres_artistes.html")

@app.route('/guide')
def guide():
    return render_template("pages/mode_emploi.html")

@app.route('/documentation')
def documentation():
    return render_template("pages/documentation_reproductibilite.html")


@app.route('/test_db')
def test_db():
    """
    Une route pour tester le branchement à la base de données du BiblioMoMA. N'a pas vocation à servir dans l'app finale.
    """
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result]
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/test_mapping')
def test_mapping():
    """
    Une deuxième route de test pour tester le modèle de données ORM mapping.py présent dans models/
    """
    try:
        artists = Artists.query.all()  
        artist_names = [artist.DisplayName for artist in artists if artist is not None]  
        return {"artists": artist_names if artist_names else "No artist found"}
    except Exception as e:
        return {"error": str(e)}
    


@app.route("/artistes/<id_artist>")
def fiche_artiste(id_artist):
    """
    Affiche la fiche détaillée d'un artiste en récupérant ses informations depuis la base de données.

    Args:
        id_artist (str): L'identifiant unique de l'artiste (WikiID).

    Returns:
        tuple: Un rendu HTML de la page "fiche_artiste.html" avec les informations de l'artiste, 
               ou une page d'erreur 404 si l'artiste n'est pas trouvé.
    
    Variables:
        artist (Artists | None): L'objet artiste correspondant à l'ID donné.
        bio (list[Artists]): Liste des artistes correspondant à l'ID (en pratique, un seul artiste).
        movements_list (list[str]): Liste des mouvements artistiques associés à l'artiste.
        genres_list (list[str]): Liste des genres artistiques associés à l'artiste.
        artworks_list (list[tuple]): Liste des œuvres de l'artiste (titre, URL de l'image).
        img (str | None): URL de la première image de l'artiste, ou None si aucune image disponible.
    """
    artist = Artists.query.filter(Artists.WikiID == id_artist).first()
    
    if not artist:
        return render_template("pages/error.html", message="Artist not found! Maybe their work are not exposed in the MoMA, or they were not referenced with their Wikidata ID."), 404
    
    bio = Artists.query.filter(Artists.WikiID == id_artist).all()

    movements_list = []
    genres_list = []
    artworks_list = db.session.execute(text(f"SELECT Title, ImageURL, id FROM Artworks WHERE ArtistWikiID = '{id_artist}'"))

    img = None

    for artist in Artists.query.filter(Artists.WikiID == id_artist).all():
        for mouvement in artist.movements:
            movements_list.append(mouvement.Label) 
        for genre in artist.genres:
            genres_list.append(genre.Label) 
        if artist.images: 
            img = artist.images[0].Link  

    return render_template(
        "pages/fiche_artiste.html", 
        artist=artist,
        bio=bio,
        genres=genres_list,
        movements=movements_list,
        artworks=artworks_list,
        image=img
    )

@app.route("/oeuvres/<id_oeuvre>")
def fiche_oeuvre(id_oeuvre):
    """Affiche la fiche détaillée d'une œuvre d'art.

    Args:
        id_oeuvre (str): L'identifiant unique de l'œuvre à afficher.

    Returns:
        tuple: 
            - Une page HTML affichant les détails de l'œuvre si elle est trouvée.
            - Une page d'erreur avec un code 404 si l'œuvre n'existe pas.
    """
    oeuvre = Artworks.query.filter(Artworks.id == id_oeuvre).first()

    if not oeuvre:
        return render_template("pages/error.html", message="Artwork not found! Maybe it is not in the MoMA collections."), 404
    


    return render_template("pages/fiche_oeuvre.html", details=oeuvre)        



@app.route('/recherche/<int:page>')
def recherche(page):
    """
    Gère la recherche et la pagination des artistes et œuvres.
    
    Args:
        page (int): Numéro de la page pour la pagination.
    
    Query Parameters:
        q (str, optional): Terme de recherche.
        type (str, optional): Filtre par type ('artistes' ou 'oeuvres').
        movement (str, optional): Filtre par mouvement artistique.
        year_filter (str, optional): Filtre par année de naissance ou de décès.
        artist_name (str, optional): Filtre par artiste (uniquement pour les œuvres).
    
    Returns:
        Flask Response: Rendu de la page "recherche.html" avec les résultats filtrés et paginés.
    """
    per_page = int(app.config["PER_PAGE"])
    query = request.args.get('q', '').strip()
    type_filtre = request.args.get('type', '').strip()
    movement = request.args.get('movement', '').strip()
    year_filter = request.args.get('year_filter', '').strip()
    artist_name = request.args.get('artist_name', '').strip()

    query_artists = Artists.query.filter(Artists.WikiID != None)
    query_artworks = Artworks.query

    if query:
        query_artists = query_artists.filter(Artists.DisplayName.ilike(f"%{query}%"))
        query_artworks = query_artworks.filter(Artworks.Title.ilike(f"%{query}%"))
    
    if movement:
        query_artists = query_artists.join(ArtistsMovements).join(Movements).filter(Movements.Label.ilike(f"%{movement}%"))
    
    if year_filter.isdigit():
        query_artists = query_artists.filter((Artists.BirthDate == int(year_filter)) | (Artists.DeathDate == int(year_filter)))
    
    if artist_name:
        query_artworks = query_artworks.join(Artists).filter(Artists.DisplayName.ilike(f"%{artist_name}%"))
    
    if type_filtre == "artistes":
        query_artworks = Artworks.query.filter(False)
    elif type_filtre == "oeuvres":
        query_artists = Artists.query.filter(False)

    artists_paginated = query_artists.paginate(page=page, per_page=per_page, error_out=False)
    artworks_paginated = query_artworks.paginate(page=page, per_page=per_page, error_out=False)

    all_items = artists_paginated.items + artworks_paginated.items
    all_items_sorted = sorted(all_items, key=lambda x: x.DisplayName if isinstance(x, Artists) else x.Title)

    return render_template(
        "pages/recherche.html",
        items=all_items_sorted,
        artists=artists_paginated,
        artworks=artworks_paginated,
        movements=Movements.query.all(),
        selected_movement=movement,
        selected_year=year_filter,
        selected_artist=artist_name
    )
