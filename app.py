from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from marshmallow import ValidationError
from models import db, Appearance, Episode, Guest
from schemas import EpisodeSchema, GuestSchema, AppearanceSchema  # Ensure these match the updated schemas

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrator = Migrate(app, db)
rest_api = Api(app)

# Instantiate schemas for serialization
single_episode_schema = EpisodeSchema()
multiple_episodes_schema = EpisodeSchema(many=True)
single_guest_schema = GuestSchema()
multiple_guests_schema = GuestSchema(many=True)
single_appearance_schema = AppearanceSchema()

# Resource for handling a list of Episodes
class EpisodeCollectionResource(Resource):
    def get(self):
        all_episodes = Episode.query.all()
        return multiple_episodes_schema.dump(all_episodes), 200

class SingleEpisodeResource(Resource):
    def get(self, episode_id):
        specific_episode = Episode.query.get(episode_id)
        if specific_episode:
            return single_episode_schema.dump(specific_episode), 200
        return {"message": "Episode not found"}, 404

# Resource for handling a list of Guests
class GuestCollectionResource(Resource):
    def get(self):
        all_guests = Guest.query.all()
        return multiple_guests_schema.dump(all_guests), 200

class SingleGuestResource(Resource):
    def get(self, guest_id):
        specific_guest = Guest.query.get(guest_id)
        if specific_guest:
            return single_guest_schema.dump(specific_guest), 200
        return {"message": "Guest not found"}, 404

# Resource for handling Appearances
class AppearanceCreationResource(Resource):
    def post(self):
        request_data = request.get_json()
        try:
            # Marshmallow's load method already creates an Appearance object
            new_appearance_entry = single_appearance_schema.load(request_data, session=db.session)
            db.session.add(new_appearance_entry)
            db.session.commit()
            return single_appearance_schema.dump(new_appearance_entry), 201
        except ValidationError as validation_error:
            return {"errors": validation_error.messages}, 400

class SingleAppearanceResource(Resource):
    def get(self, appearance_id):
        specific_appearance = Appearance.query.get(appearance_id)
        if specific_appearance:
            return single_appearance_schema.dump(specific_appearance), 200
        return {"message": "Appearance not found"}, 404

# Register RESTful routes
rest_api.add_resource(EpisodeCollectionResource, '/episodes')
rest_api.add_resource(SingleEpisodeResource, '/episodes/<int:episode_id>')
rest_api.add_resource(GuestCollectionResource, '/guests')
rest_api.add_resource(SingleGuestResource, '/guests/<int:guest_id>')
rest_api.add_resource(AppearanceCreationResource, '/appearances')
rest_api.add_resource(SingleAppearanceResource, '/appearances/<int:appearance_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
