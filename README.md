# <H1 align="center">📚BiblioMoMA🎨</H1>

BiblioMoMA est une application web qui propose une visite bibliographique à travers les collections du *Museum of Modern Art*. BiblioMoMA, permet à l'utilisateur de visualiser des informations relatives à la vie et au travail d'un artiste lorsqu'il ou elle recherche ou clique sur une œuvre, ainsi qu'une vourte bibliographie académique. Simple d'accès, BiblioMoMA se veut ouvert à tous les publics, du collégien au chercheur en histoire de l'art.

<details>
  <summary>Table des matières</summary>
  <ol>
    <li><a href=#Lequipe>L'équipe</a></li>
    <li><a href=#Techno>Technologies utilisées</a></li>
    <li><a href=#Installation>Installation</a></li>
    <li><a href=#Contribution>Contribution</a></li>
    <li><a href=#Contact>Contact</a></li>
</ol>
</details>

<span id=#Lequipe></a>
## 👩‍💻L'équipe 👨‍💻 : 

L'application BiblioMoMA a été créer par : 
- Sidonie BASSAISTEGUY 
- Camille BATARD
- Juliette BENGUIGUI 
- Adonis DULAURENT

du master 2 Technologies Appliquées à l'Histoire de l'École Nationale des Chartes.

<a href="https://github.com/Adonis-Dulaurent/BiblioMoma/graphs/contributors">
<img src="https://contrib.rocks/image?repo=Adonis-Dulaurent/BiblioMoma" alt="contrib.rocks image"/>
</a>
<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<span id=#Techno></a>
## 🖌️ Technologies utilisées : 

- **💻 Back-end**:
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
 [![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)](#)

- **🌐 Front-End**:
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3)
![JavaScript](https://img.shields.io/badge/-JavaScript-f4fc00?style=flat&logo=javascript&logoColor=black)

- **⛁ Base de donnés**:![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)

- **⚙️ outils collaboratifs** :
  ![Git](https://img.shields.io/badge/-Git-black?style=flat&logo=git)
  ![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github) 

  <p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<span id=#Installation></a>
## 🖼️ Installation

1. Cloner le repository : 

```bash
git clone git@github.com:Adonis-Dulaurent/BiblioMoma.git
cd <BiblioMoma>
```

2. Mise en place de l'environnement :

```bash
 virtualenv env -p python3
 source ./env/bin/activate
```

3. Installation des dépendances :

```bash
pip install -r requirements.txt
```

4. Dans le dossier BiblioMoma, créer le fichier .env et y coller le contenu suivant :

```bash
SECRET_KEY = inserer_clef_secrete_choisie
DEBUG=True
SQLALCHEMY_DATABASE_URI=sqlite:////chemin/de/sa/base/de/donnees.db
SQLALCHEMY_ECHO=False
WTF_CSRF_ENABLE=True
PER_PAGE = 50
```

5. Lancer l'application : 

```bash
python3 run.py
```

Vous pouvez maintenant utiliser l'application ! 

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<span id=#Contribution></a>
## 👩‍🎨Contribution 👨‍🎨:

Si vous voulez rejoindre l'aventure BiblioMoma. Vous pouvez contribuer en suivant ces étapes : 

1. Créer un dépôt (*fork*)

2. Créer une branche pour vos changements (`git checkout -b feature`)

3. Créer un commit avec vos changements (`git commit-m'[feature]'addition of this feature`)

4. Pousser votre branch (`git push origin feature`)

5. Créer un Pull Request 

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<span id=#Contact></a>
## Contact
Sidonie BASSAISTEGUY - sidonie.bassaisteguy@chartes.psl.eu

Camille BATARD - camille.batard@chartes.psl.eu

Juliette BENGUIGUI - juliette.benguigui@chartes.psl.eu

Adonis DULAURENT - adonis.dulaurent@chartes.psl.eu

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>
