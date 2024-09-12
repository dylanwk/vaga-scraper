import mongoengine as me
from datetime import datetime
from bson import ObjectId


me.connect(host="mongodb+srv://dwalkman:dwalkman@cluster0.ctofdja.mongodb.net/")

class Location(me.EmbeddedDocument):
    country = me.StringField(required=True)
    city = me.StringField(required=True)
    address = me.StringField()
    coordinates = me.PointField()  # For storing latitude and longitude


class Listing(me.Document):
    meta = {"collection": "Listing"}

    id = me.ObjectIdField(primary_key=True, required=True, default=ObjectId)
    title = me.StringField(required=True)
    price = me.IntField(required=True, min_value=0)  
    link = me.URLField(required=True)  
    image_src = me.URLField(required=True)  
    amenities = me.ListField(me.StringField(), required=True)  
    bed_count = me.IntField(required=True, min_value=0)
    bathroom_count = me.IntField(required=True, min_value=0)
    guest_count = me.IntField(required=True, min_value=0)
    location_attractions = me.ListField(me.StringField(), required=True)  
    location = me.EmbeddedDocumentField(Location, required=True)  # Embed Location document
    created_at = me.DateTimeField(default=datetime.now())  
    descriptors = me.ListField(me.StringField())  
    description = me.StringField()
    user_id = me.ObjectIdField(required=True)  
    property_type = me.StringField(required=True, choices=["Apartment", "Entire House"])
    filters = me.ListField(me.StringField(), choices=["Coastal", "Scenic", "Modern", "Downtown", "Pools", "Workspaces", "Cafés Nearby", "Design", "Luxury", "Balconies", "High-Speed Wifi"]
)  


def create_listing(listing):
    listing.save()
    print(f"Listing created with Title: {listing.title}")
