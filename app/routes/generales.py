from ..app import app, db
from flask import render_template, abort
from flask import jsonify
from sqlalchemy import text 
from ..models.mapping import *
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import sessionmaker



@app.route('/')
@app.route('/home')
def accueil():
    return render_template("pages/index.html")

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
        return render_template("pages/error.html", message="Artiste non trouvé"), 404
    
    bio = Artists.query.filter(Artists.WikiID == id_artist).all()

    movements_list = []
    genres_list = []
    artworks_list = db.session.execute(text(f"SELECT Title, ImageURL, id FROM Artworks WHERE ArtistWikiID = '{id_artist}'"))

    img = None

    for artist in Artists.query.filter(Artists.WikiID == id_artist).all():
        for mouvement in artist.movements:
            movements_list.append(mouvement.Label) #FIXME : ici mettre un message si pas de mouvement artistique affilié
        for genre in artist.genres:
            genres_list.append(genre.Label) #FIXME : ici mettre un message si pas de genre affilié
        if artist.images: 
            img = artist.images[0].Link  # Ici on prend la première image, l'important est d'en avoir une si elle existe
            
    
     
    return render_template(
        "pages/fiche_artiste.html", 
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
        return render_template("pages/error.html", message="Artiste non trouvé"), 404
    


    return render_template("pages/fiche_oeuvre.html", details=oeuvre)        
