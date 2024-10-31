from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# CREATING THE CLASSES

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete")
    
    # Adding validation
    @validates('date')
    def validate_date(self, key, value):
        if not value:
            raise ValueError("Date is required.")
        return value

    @validates('number')
    def validate_number(self, key, value):
        if value <= 0:
            raise ValueError("Episode number must be a positive integer.")
        return value
    
    def __repr__(self):
        return f'<Episode {self.number} on {self.date}>'

# Guest class
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete")

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Guest name cannot be empty.")
        return value

    @validates('occupation')
    def validate_occupation(self, key, value):
        if not value:
            raise ValueError("Guest occupation cannot be empty.")
        return value
    
    def __repr__(self):
        return f'<Guest {self.name}, Occupation: {self.occupation}>'

# Appearance class
class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)

    # Validation
    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value

    @validates('guest_id')
    def validate_guest_id(self, key, value):
        if not value:
            raise ValueError("Guest ID is required.")
        return value

    @validates('episode_id')
    def validate_episode_id(self, key, value):
        if not value:
            raise ValueError("Episode ID is required.")
        return value
    
    def __repr__(self):
        return f'<Appearance: Guest ID {self.guest_id}, Episode ID {self.episode_id}, Rating {self.rating}>'
