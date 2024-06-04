from app import const

BASE_ID = const.AIRTABLE_MAP_BY_GEOGRAPHIC_AREA_BASE_ID

GEOGRAPHIC_AREAS_TABLE_NAME = "Geographic Areas"
AREA_CONTACT_TABLE_NAME = "Area Contact"
AREA_TARGET_COMMUNITY_TABLE_NAME = "Area Target Community"
AUTO_RESPONSE_EMAIL_TEMPLATE = "Auto-Response Email Template"


class AirtableGeographicAreaTypes:
    AREA_TYPE_CITY = "City"
    AREA_TYPE_POLYGON = "Polygon"
    AREA_TYPE_REGION = "Region"
    AREA_TYPE_STATE = "State"
    AREA_TYPE_COUNTRY = "Country"
    AREA_TYPE_DEFAULT_US = "Default (US)"
    AREA_TYPE_DEFAULT_INTERNATIONAL = "Default (International)"
