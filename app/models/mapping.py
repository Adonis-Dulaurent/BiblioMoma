from ..app import app, db 

# Nos tables associatives pour lier les artistes à leurs genres ou mouvements artistiques 
ArtistsMovements = db.Table(
    "ArtistsMovements",
    db.Column('ArtistID', db.String(100), db.ForeignKey("Artists.WikiID"), primary_key=True),
    db.Column('MovementID', db.String(100), db.ForeignKey("Movements.WikiID"), primary_key=True)
)

ArtistsGenres = db.Table(
    "ArtistsGenres",
    db.Column('ArtistID', db.String(100), db.ForeignKey("Artists.WikiID"), primary_key=True),
    db.Column('GenreID', db.String(100), db.ForeignKey("Genres.WikiID"), primary_key=True)
)


# Définition des classes pour les tables principales 

class Artists(db.Model):
    __tablename__ = "Artists"

    DisplayName = db.Column(db.Text)
    BirthDate = db.Column(db.Integer)
    DeathDate = db.Column(db.Integer)
    Nationality = db.Column(db.Text)
    Gender = db.Column(db.Text)
    WikiID = db.Column(db.String(100), primary_key=True)
    ulan = db.Column(db.String(100))

    artworks = db.relationship(
        "Artworks", 
        backref="Artists",
        lazy='joined'    
    )

    images = db.relationship(
        "ArtistsImages",
        backref="Artists",
        lazy=True 
    )

    artistsmovements = db.relationship(
        "Movements",
        secondary=ArtistsMovements,
        backref="Artists"
    )

    genres = db.relationship(
        "Genres",
        secondary=ArtistsGenres,
        backref="Artists"
    )

    def __repr__(self):
        return f"<Artist id={self.WikiID}, name={self.DisplayName}>"


class Artworks(db.Model): 
    __tablename__ = "Artworks"

    Title = db.Column(db.Text)
    Artist = db.Column(db.Text)
    ConstituentID = db.Column(db.String(100), primary_key=True)
    BeginningDate = db.Column(db.Integer)
    EndDate = db.Column(db.Integer)
    Medium = db.Column(db.Text)
    Dimensions = db.Column(db.Text)
    CreditLine = db.Column(db.Text)
    Classification = db.Column(db.Text)
    Department = db.Column(db.Text)
    DateAcquired = db.Column(db.String(100))
    url = db.Column(db.Text)
    ImageURL = db.Column(db.Text)
    
    # clé étrangère 
    ArtistWikiID = db.Column(
        db.String(100),
        db.ForeignKey("Artists.WikiID") #FIXME ici voir si la relation avec Artists s'est bien faite car on ne peut pas mettre deux primary keys dans une classe SQLalchemy donc possible de que soit faussé. 
    )
    
    # artist = db.relationship("Artists", backref="artworks", lazy="joined")  # TEST

    def __repr__(self):
        return f"<Artwork name={self.Title}>"


class ArtistsImages(db.Model):
    __tablename__ = "ArtistsImages"

    Link = db.Column(db.Text, primary_key=True)
    

    # clé étrangère
    ArtistID = db.Column(
        db.String(100),
        db.ForeignKey("Artists.WikiID")
        )

class Movements(db.Model):
    __tablename__ = "Movements"

    WikiID = db.Column(db.String(100))
    Label = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f"<Mouvement={self.Label}>"

class Genres(db.Model):
    __tablename__ = "Genres"

    WikiID = db.Column(db.String(100))
    Label = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f"<Genre={self.Label}>"

