from ..app import app, db
from flask import render_template
from flask import jsonify
from sqlalchemy import text
from ..models.mapping import *


@app.route('/')
@app.route('/home')
def accueil():
    return render_template("pages/index.html")

@app.route('/cent_oeuvres_artistes')
def cent_oeuvres_artistes():
    return render_template("pages/cent_oeuvres_artistes.html")

@app.route('/documentation_reproductibilite')
def documentation_reproductibilite():
    return render_template("pages/documentation_reproductibilite.html")

@app.route('/mode_emploi')
def mode_emploi():
    return render_template("pages/mode_emploi.html")

@app.route('/recherche_avancee')
def recherche_avancee():
    return render_template("pages/recherche_avancee.html")

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



