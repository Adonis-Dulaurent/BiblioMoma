from ..app import app, db
from flask import render_template
from flask import jsonify
from sqlalchemy import text
from ..models.mapping import *
from sqlalchemy.orm import joinedload


@app.route('/')
def accueil():
    return render_template("pages/index.html")

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
    

from sqlalchemy.orm import joinedload

@app.route('/api/artists/<artist_id>/artworks')
def get_artist_artworks(artist_id):
    artist = Artists.query.options(joinedload(Artists.artworks)).filter_by(WikiID=artist_id).first()

    if not artist:
        return jsonify({"error": "No artist found"}), 404

    print(f"Nombre d'œuvres trouvées pour {artist.DisplayName} : {len(artist.artworks)}")  # DEBUG

    return jsonify({
        "id": artist.WikiID,
        "name": artist.DisplayName,
        "birth": artist.BirthDate,
        "death": artist.DeathDate,
        "nationality": artist.Nationality,
        "artworks": [{"title": aw.Title, "medium": aw.Medium} for aw in artist.artworks]
    })




