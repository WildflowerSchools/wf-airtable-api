from typing import Callable, Optional

from pydantic import BaseModel

from . import response as response_models
from . import educators_schools as educators_schools_models
from . import languages as languages_models
from . import montessori_certifications as montessori_certifications_models
from .response import APIData
from ..airtable import educators as airtable_educator_models
from ..airtable import educators_schools as airtable_educators_schools_models
from ..airtable import languages as airtable_languages_models
from ..airtable import montessori_certifications as airtable_montessori_certifications_models

MODEL_TYPE = 'educator'


class APIEducatorFields(BaseModel):
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[list[str]] = None
    details: Optional[str] = None
    home_address: Optional[str] = None
    target_community: Optional[list[str]] = None
    stage: Optional[str] = None
    visioning_album_complete: Optional[bool] = None
    affiliation_agreement_url: Optional[str] = None
    current_roles: Optional[list[str]] = None
    source: Optional[list[str]] = None
    source_other: Optional[str] = None
    race_and_ethnicity: Optional[list[str]] = None
    race_and_ethnicity_other: Optional[str] = None
    educational_attainment: Optional[str] = None
    income_background: Optional[str] = None
    gender: Optional[str] = None
    lgbtqia_identifying: Optional[bool] = None
    pronouns: Optional[str] = None
    montessori_certified: Optional[bool] = None


class APIEducatorRelationships(BaseModel):
    educators_schools: Optional[response_models.APILinksAndData] = None
    assigned_partners: Optional[response_models.APILinks] = None
    languages: Optional[response_models.APILinksAndData] = None
    montessori_certifications: Optional[response_models.APILinksAndData] = None


class APIEducatorResponse(response_models.APIResponse):
    fields: APIEducatorFields

    @classmethod
    def from_airtable_educator(cls,
                               airtable_educator: airtable_educator_models.AirtableEducatorResponse,
                               url_path_for: Callable):
        fields = APIEducatorFields(
            full_name=airtable_educator.fields.full_name,
            first_name=airtable_educator.fields.first_name,
            last_name=airtable_educator.fields.last_name,
            email=airtable_educator.fields.email,
            details=airtable_educator.fields.details,
            home_address=airtable_educator.fields.home_address,
            target_community=airtable_educator.fields.target_community,
            stage=airtable_educator.fields.stage,
            visioning_album_complete=airtable_educator.fields.visioning_album_complete,
            visioning_album=airtable_educator.fields.visioning_album,
            current_roles=airtable_educator.fields.current_roles,
            source=airtable_educator.fields.source,
            source_other=airtable_educator.fields.source_other,
            race_and_ethnicity=airtable_educator.fields.race_and_ethnicity,
            race_and_ethnicity_other=airtable_educator.fields.race_and_ethnicity_other,
            educational_attainment=airtable_educator.fields.educational_attainment,
            income_background=airtable_educator.fields.income_background,
            gender=airtable_educator.fields.gender,
            lgbtqia_identifying=airtable_educator.fields.lgbtqia_identifying,
            pronouns=airtable_educator.fields.pronouns,
            montessori_certified=airtable_educator.fields.montessori_certified
        )

        educators_schools_data = []
        if airtable_educator.fields.educators_schools is not None:
            for d in airtable_educator.fields.educators_schools:
                if isinstance(d, airtable_educators_schools_models.AirtableEducatorsSchoolsResponse):
                    educators_schools_data.append(APIData(
                        id=d.id,
                        type=educators_schools_models.MODEL_TYPE,
                        meta=educators_schools_models.APIEducatorsSchoolsFields(
                            educator_name=d.fields.educator_name,
                            school_name=d.fields.school_name,
                            role=d.fields.role,
                            currently_active=d.fields.currently_active,
                            start_date=d.fields.start_date,
                            end_date=d.fields.end_date
                        )))
                else:
                    educators_schools_data.append(d)

        educators_languages_data = []
        if airtable_educator.fields.languages is not None:
            for d in airtable_educator.fields.languages:
                if isinstance(d, airtable_languages_models.AirtableLanguageResponse):
                    educators_languages_data.append(APIData(
                        id=d.id,
                        type=languages_models.MODEL_TYPE,
                        meta=languages_models.APILanguagesFields(
                            full_name=d.fields.full_name,
                            language=d.fields.language,
                            language_dropdown=d.fields.language_dropdown,
                            language_other=d.fields.language_other,
                            is_primary_language=d.fields.is_primary_language
                        )))
                else:
                    educators_languages_data.append(d)

        educators_montessori_certifications_data = []
        if airtable_educator.fields.montessori_certifications is not None:
            for d in airtable_educator.fields.montessori_certifications:
                if isinstance(d, airtable_montessori_certifications_models.AirtableMontessoriCertificationResponse):
                    educators_montessori_certifications_data.append(APIData(
                        id=d.id,
                        type=montessori_certifications_models.MODEL_TYPE,
                        meta=montessori_certifications_models.APIMontessoriCertificationsFields(
                            full_name=d.fields.full_name,
                            year_certified=d.fields.year_certified,
                            certification_levels=d.fields.certification_levels,
                            certifier=d.fields.certifier,
                            certifier_other=d.fields.certifier_other,
                            certification_status=d.fields.certification_status
                        )))
                else:
                    educators_montessori_certifications_data.append(d)

        relationships = APIEducatorRelationships(
            educators_schools=response_models.APILinksAndData(
                links={'self': url_path_for("get_educator_schools", educator_id=airtable_educator.id)},
                data=educators_schools_data),
            assigned_partners=response_models.APILinks(
                links={'self': url_path_for("get_educator_guides", educator_id=airtable_educator.id)}),
            languages=response_models.APILinksAndData(
                links=None,
                data=educators_languages_data),
            montessori_certifications=response_models.APILinksAndData(
                links=None,
                data=educators_montessori_certifications_data)
        )
        links = response_models.APILinks(
            links={'self': url_path_for("get_educator", educator_id=airtable_educator.id)}
        )
        return response_models.APIResponse(
            id=airtable_educator.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links
        )


class ListAPIEducatorResponse(BaseModel):
    __root__: list[APIEducatorResponse]

    @classmethod
    def from_airtable_educators(cls,
                                airtable_educators: airtable_educator_models.ListAirtableEducatorResponse,
                                url_path_for: Callable):
        educator_responses = []
        for e in airtable_educators.__root__:
            educator_responses.append(
                APIEducatorResponse.from_airtable_educator(
                    airtable_educator=e,
                    url_path_for=url_path_for))

        return educator_responses
