import os

AIRTABLE_API_KEY = os.getenv(
    "AIRTABLE_API_KEY", None)

AIRTABLE_SCHOOL_DB_BASE_ID = os.getenv(
    "AIRTABLE_SCHOOL_DB_BASE_ID", 'appldwtPcWL8zl3OP'  # Defaults to the STAGING instance
)

AIRTABLE_MAP_BY_GEOGRAPHIC_AREA_BASE_ID = os.getenv(
    "AIRTABLE_MAP_BY_GEOGRAPHIC_AREA_BASE_ID", 'appoXMtqc5TYmH0ai'
)

AUTH0_AUDIENCE = os.getenv(
    "AUTH0_AUDIENCE", None)

AUTH0_DOMAIN = os.getenv(
    "AUTH0_DOMAIN", None)

GOOGLE_CLOUD_API_KEY = os.getenv(
    "GOOGLE_CLOUD_API_KEY", None
)

STAGE = os.getenv(
    "STAGE", 'dev')
