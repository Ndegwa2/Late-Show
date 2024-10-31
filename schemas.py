from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from models import Appearance, Episode, Guest
from flask import url_for

class AppearanceSchema(SQLAlchemyAutoSchema):
    """Schema for the Appearance model with HATEOAS links."""
    links = fields.Method("generate_appearance_links")

    class Meta:
        model = Appearance
        include_fk = True
        load_instance = True

    rating = fields.Int(required=True)

    @validates('rating')
    def check_rating(self, value):
        """Validate that rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    def generate_appearance_links(self, obj):
        """Generate HATEOAS links for the Appearance resource."""
        return {
            "self": url_for("singleappearanceresource", appearance_id=obj.id, _external=True),
            "episode": url_for("singleepisoderesource", episode_id=obj.episode_id, _external=True),
            "guest": url_for("singleguestresource", guest_id=obj.guest_id, _external=True),
        }

class EpisodeSchema(SQLAlchemyAutoSchema):
    """Schema for the Episode model with HATEOAS links."""
    appearance_list = fields.Nested('AppearanceSchema', many=True, exclude=("episode",))
    links = fields.Method("generate_episode_links")

    class Meta:
        model = Episode
        include_fk = True
        load_instance = True

    def generate_episode_links(self, obj):
        """Generate HATEOAS links for the Episode resource."""
        return {
            "self": url_for("singleepisoderesource", episode_id=obj.id, _external=True),
            "appearances": url_for("appearancecreationresource", episode_id=obj.id, _external=True),
        }

class GuestSchema(SQLAlchemyAutoSchema):
    """Schema for the Guest model with HATEOAS links."""
    appearance_list = fields.Nested('AppearanceSchema', many=True, exclude=("guest",))
    links = fields.Method("generate_guest_links")

    class Meta:
        model = Guest
        include_fk = True
        load_instance = True

    def generate_guest_links(self, obj):
        """Generate HATEOAS links for the Guest resource."""
        return {
            "self": url_for("singleguestresource", guest_id=obj.id, _external=True),
            "appearances": url_for("appearancecreationresource", guest_id=obj.id, _external=True),
        }
