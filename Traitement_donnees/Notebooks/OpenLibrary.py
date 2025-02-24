
import requests
import json
import time

# Pour modifier le sujet de la requette, il faut changer le mot avant le .json

base_url = "https://openlibrary.org/subjects/art.json"
limit = 1000  # Maximum autorisé
offset = 0
all_data = []

while True:
    print(f"Fetching data with offset {offset}...")  # Debugging log
    
    try:
        response = requests.get(f"{base_url}?limit={limit}&offset={offset}", timeout=10)  # Ajout d'un timeout

        if response.status_code != 200:
            print(f"Erreur {response.status_code} : {response.text}")
            break
        
        data = response.json()
        works = data.get("works", [])

        if not works:
            print("Plus de résultats à récupérer.")
            break  # Sortir si plus de données

        all_data.extend(works)
        print(f"Récupérés : {len(all_data)} travaux")  # Afficher la progression

        offset += limit  # Passer à la page suivante
        time.sleep(1)  # Pause pour éviter d'être bloqué par l'API (rate limiting)

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")
        break

print(f"Nombre total de résultats récupérés : {len(all_data)}")

# Sauvegarde en JSON
with open("art_subject_data.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("Données sauvegardées dans art_subject_data.json")