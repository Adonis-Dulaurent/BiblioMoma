from ..app import app, db
from flask import render_template, abort
from flask import jsonify
from sqlalchemy import text 
from ..models.mapping import *


import requests
from flask import jsonify

@app.route('/oeuvres/<int:id_oeuvre>/bibliography')
def get_oeuvre_biblio(id_oeuvre):
    """Récupère la bibliographie associée à une œuvre via OpenAlex."""

    oeuvre = Artworks.query.filter(Artworks.id == id_oeuvre).first()
    if not oeuvre:
        return render_template("pages/error.html", message="L'artiste n'est pas référencé dans la base de données"), 404

    query_title = oeuvre.Title.replace(" ", "+")  # Formatage du titre pour la requête
    base_url = f" https://api.openalex.org/works?page=1&filter=primary_topic.field.id:fields/12,default.search:{query_title}&sort=relevance_score:desc&per_page=10"

    response = requests.get(base_url)
    if response.status_code != 200:
        return render_template("pages/error.html", message="La requête n'a pas fonctionné"), 404

    data = response.json()
    results = []
    for book in data.get("results"):
        info = {
            "OpenAlex ID" : book.get("id"),
            "Title" : book.get("title"),
            "Publication year" : book.get("publication_year")
        }
        results.append(info)

    # user = int(input("combien voulez vous de livre"))
    # option_1 = results[0:user]

    results = results[0:10]

    return render_template("pages/bibliography.html", results=results)




@app.route('/artistes/<id_artiste>/bibliography')
def get_artiste_biblio(id_artiste):
    """Récupère la bibliographie associée à un artiste via OpenAlex."""

    artiste = Artists.query.filter(Artists.WikiID == id_artiste).first()
    if not artiste:
        return jsonify({"error": "Artiste non trouvé"}), 404

    query_name = artiste.Name.replace(" ", "+")
    base_url = f"https://api.openalex.org/works?filter=authorships.institutions.display_name.search:{query_name}&sort=cited_by_count:desc&per_page=10"

    response = requests.get(base_url)
    if response.status_code != 200:
        return render_template("pages/error.html", message="La requête n'a pas fonctionné"), 404

    data = response.json()

    bibliography = [
        {
            "title": work.get("title", "Titre inconnu"),
            "url": work.get("id", "#")
        }
        for work in data.get("results", [])
    ]

    return jsonify({"results": bibliography})

