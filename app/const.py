import os

AIRTABLE_API_KEY = os.getenv(
    "AIRTABLE_API_KEY", None)

AUTH0_AUDIENCE = os.getenv(
    "AUTH0_AUDIENCE", None)

AUTH0_DOMAIN = os.getenv(
    "AUTH0_DOMAIN", None)

STAGE = os.getenv(
    "STAGE", 'dev')
