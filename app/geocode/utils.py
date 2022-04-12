from typing import Union

from haversine import haversine, Unit
from shapely import geometry

from app.airtable.base_map_by_geographic_area.const import AirtableGeographicAreaTypes
from app.geocode.geocode_models import Place, LatLngLiteral
from app.models.geo_area_contacts import APIGeoAreaContactData
from app.models.geo_area_target_communities import APIGeoAreaTargetCommunityData


def distance_between_points(a: LatLngLiteral, b: LatLngLiteral):
    return haversine(a.as_tuple(), b.as_tuple(), unit=Unit.MILES)


def distance_between_places(a: Place, b: Place):
    return distance_between_points(a.geometry.location, b.geometry.location)


def is_place_contained_within(a: Place, b: Place):
    return b.geometry.viewport.northeast.lat >= a.geometry.location.lat >= b.geometry.viewport.southwest.lat and b.geometry.viewport.northeast.lng >= a.geometry.location.lng >= b.geometry.viewport.southwest.lng


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


def get_geo_area_nearest_to_place(
        place: Place, geo_areas: Union[list[APIGeoAreaContactData], list[APIGeoAreaTargetCommunityData]]):
    default_geo_area = None
    default_international_geo_area = None
    city_geo_areas = []
    polygon_geo_areas = []
    region_geo_areas = []
    state_geo_areas = []
    country_geo_areas = []

    for ga in geo_areas:
        if ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_DEFAULT_US:
            default_geo_area = ga

        elif ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_DEFAULT_INTERNATIONAL:
            default_international_geo_area = ga

        elif ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_POLYGON:
            polygon_geo_areas.append(ga)

        elif ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_CITY:
            city_geo_areas.append(ga)

        elif ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_REGION:
            region_geo_areas.append(ga)

        elif ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_STATE:
            state_geo_areas.append(ga)

        elif ga.fields.area_type == AirtableGeographicAreaTypes.AREA_TYPE_COUNTRY:
            country_geo_areas.append(ga)

    geo_area = None

    geo_areas_near_cities = []
    for ga in city_geo_areas:
        if (is_place_within_radius(place, ga.geocode(), ga.fields.city_radius)):
            geo_areas_near_cities.append(ga)

    if len(geo_areas_near_cities) > 0:
        geo_area = min(geo_areas_near_cities, key=lambda ga: distance_between_places(place, ga.geocode()))

    if geo_area is None:
        geo_point = geometry.Point(place.geometry.location.lat, place.geometry.location.lng)

        for ga in polygon_geo_areas:
            str_point_list = ga.fields.polygon_coordinates.strip('(').strip(')').split(",")

            def str_point_to_geo_point(s):
                parts = s.strip(' ').split(' ')
                return geometry.Point(float(parts[1]), float(parts[0]))

            geo_point_list = list(map(str_point_to_geo_point, str_point_list))
            polygon = geometry.Polygon(geo_point_list)
            if polygon.contains(geo_point):
                geo_area = ga
                break

    if geo_area is None:
        for ga in region_geo_areas:
            if (is_place_contained_within(place, ga.geocode())):
                geo_area = ga
                break

    if geo_area is None:
        for ga in state_geo_areas:
            if (is_place_within_state(place, ga.geocode())):
                geo_area = ga
                break

    if geo_area is None:
        for ga in country_geo_areas:
            if (is_place_within_country(place, ga.geocode())):
                geo_area = ga
                break

    if geo_area is None:
        if place.get_country_component().short_name == "US":
            geo_area = default_geo_area
        else:
            geo_area = default_international_geo_area

    return geo_area
