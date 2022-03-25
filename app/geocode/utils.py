from haversine import haversine, Unit

from app.geocode.geocode_models import Place, LatLngLiteral


def distance_between_points(a: LatLngLiteral, b: LatLngLiteral):
    return haversine(a.as_tuple(), b.as_tuple(), unit=Unit.MILES)


def distance_between_places(a: Place, b: Place):
    return distance_between_points(a.geometry.location, b.geometry.location)


def is_place_contained_within(a: Place, b: Place):
    return a.geometry.viewport.northeast.lat >= b.geometry.location.lat >= a.geometry.viewport.southwest.lat and \
        a.geometry.viewport.northeast.lng >= b.geometry.location.lng >= a.geometry.viewport.southwest.lng


def is_place_within_radius(a: Place, b: Place, radius: int):
    return distance_between_places(a, b) <= radius


def is_place_within_state(a: Place, state: Place):
    a_state = a.get_state_component()
    b_state = state.get_state_component()

    if a_state is None or b_state is None:
        return False

    return a_state.short_name == b_state.short_name


def is_place_within_country(a: Place, country: Place):
    a_country = a.get_country_component()
    b_country = country.get_country_component()

    if a_country is None or b_country is None:
        return False

    return a_country.short_name == b_country.short_name
