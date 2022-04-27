import re
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
    return (
        b.geometry.viewport.northeast.lat >= a.geometry.location.lat >= b.geometry.viewport.southwest.lat
        and b.geometry.viewport.northeast.lng >= a.geometry.location.lng >= b.geometry.viewport.southwest.lng
    )


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
    place: Place, geo_areas: Union[list[APIGeoAreaContactData], list[APIGeoAreaTargetCommunityData]]
):
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
        if is_place_within_radius(place, ga.geocode(), ga.fields.city_radius):
            geo_areas_near_cities.append(ga)

    if len(geo_areas_near_cities) > 0:
        geo_area = min(geo_areas_near_cities, key=lambda ga: distance_between_places(place, ga.geocode()))

    if geo_area is None:
        geo_point = geometry.Point(place.geometry.location.lat, place.geometry.location.lng)

        for ga in polygon_geo_areas:
            # Example polygon str format:
            #
            # POLYGON ((-73.9010989 40.997664, -74.3370459 41.1888957, -74.551168 41.2934439,
            # -74.70173 41.3622667, -74.7850821 41.3274224, -75.1418139 40.9865643, -75.2108798 40.5854214,
            # -74.9472072 40.3178983, -74.1891479 40.4517927, -74.2639676 40.4960505, -74.247494 40.5220241,
            # -74.2502596 40.5348199, -74.2353817 40.5579361, -74.2143148 40.5591341, -74.2037494 40.5923079,
            # -74.2011374 40.6325788, -74.1849067 40.6464003, -74.1400525 40.6422367, -74.0952643 40.6488871,
            # -74.0560421 40.6522048, -74.0336221 40.6935376, -74.0136887 40.7624537, -73.9336322 40.8769537,
            # -73.9010989 40.997664))
            match = re.match(r"(?:[POLYGON]+)?(?:[\s\(]+)?([-+\d\.\s,]+)", ga.fields.polygon_coordinates)
            if match is None:
                continue

            str_point_list = match.group(1)
            str_point_list = str_point_list.strip().split(",")

            def str_point_to_geo_point(s):
                parts = s.strip().split(" ")
                return geometry.Point(float(parts[1]), float(parts[0]))

            geo_point_list = list(map(str_point_to_geo_point, str_point_list))
            polygon = geometry.Polygon(geo_point_list)
            if polygon.contains(geo_point):
                geo_area = ga
                break

    if geo_area is None:
        for ga in region_geo_areas:
            if is_place_contained_within(place, ga.geocode()):
                geo_area = ga
                break

    if geo_area is None:
        for ga in state_geo_areas:
            if is_place_within_state(place, ga.geocode()):
                geo_area = ga
                break

    if geo_area is None:
        for ga in country_geo_areas:
            if is_place_within_country(place, ga.geocode()):
                geo_area = ga
                break

    if geo_area is None:
        if place.get_country_component().short_name == "US":
            geo_area = default_geo_area
        else:
            geo_area = default_international_geo_area

    return geo_area
