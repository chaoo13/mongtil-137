from google.appengine.ext import ndb


class Route(ndb.Model):
    from_airport = ndb.StringProperty()
    airline = ndb.StringProperty()
    to_airport = ndb.StringProperty()
    to_city = ndb.StringProperty()


def input_route(from_airport, airline, to_airport, to_city):
    route = Route(from_airport=from_airport, airline=airline, to_airport=to_airport, to_city=to_city)
    route.put()