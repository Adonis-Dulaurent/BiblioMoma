import requests
from flask import jsonify, request
from sqlalchemy import text 

from ..app import app, db
from .generales import *
from ..models.mapping import *




@app.route('/oeuvres/<id_oeuvre>/bibliography')
def get_oeuvre_biblio(id_oeuvre):
    """Renvoie la bibliographie en JSON via OpenAlex."""

    oeuvre = Artworks.query.filter(Artworks.id == id_oeuvre).first()
    if not oeuvre:
        return jsonify({"error": "The Artwork is not referenced"}), 404

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





@app.route('/artistes/<id_artist>/bibliography')
def get_artiste_biblio(id_artist):
    """Renvoie la bibliographie en JSON via OpenAlex."""

    artiste = Artists.query.filter(Artists.WikiID == id_artist).first()
    if not artiste:
        return jsonify({"error": "The artist is not referenced"}), 404

    query_title = artiste.DisplayName.replace(" ", "+")
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
            "Authors" : [author.get("author", {}).get("display_name", "") for author in book.get("authorships")],
            "Publisher" : publisher,
            "Type" : book.get("type"),
            "OpenAccess" : book.get("open_access").get("oa_status")   

        }
        results.append(result)
    return jsonify(results)



