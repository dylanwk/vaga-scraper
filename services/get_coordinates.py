from geopy.geocoders import Nominatim
import mongoengine as me


def get_coordinates(location: str):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode({location})
    if location:
        return {'type': 'Point', 'coordinates': [location.longitude, location.latitude]}
    else:
        return None


class Location(me.Document):
    coordinates = me.PointField()
