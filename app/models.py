# functions that you wish to incorporate in the route files
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    relationship = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name, relationship):
        self.name = name
        self.saved = []
        self.relationship = relationship

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        d = {}
        d["saved"] = []
        if len(self.saved) > 0:
            for city in self.saved:
                city_id = city.id
                city_name = city.name
                d["saved"].append(city_name)
        d["id"] = self.id
        d["name"] = self.name
        d["relationship"] = self.relationship
        return d


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    listed = db.relationship('User',
            secondary = 'watchlist',
            backref = 'saved',
            lazy = 'dynamic'
    )
    
    def __init__(self, name):
        self.name = name

    def save_city(self):
        db.session.add(self)
        db.session.commit()

    def addToWatch(self, user):
        self.listed.append(user)
        db.session.commit()

    def removeFromWatch(self, user):
        self.listed.remove(user)
        db.session.commit()
    

watchlist = db.Table(
    "watchlist",
    db.Column('user_id', db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column('city_id', db.Integer, db.ForeignKey("city.id"), nullable=False)
)