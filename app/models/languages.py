from typing import Optional

from pydantic import BaseModel

MODEL_TYPE = 'languages'


class APILanguagesFields(BaseModel):
    full_name: Optional[str] = None
    language: Optional[str] = None
    language_dropdown: Optional[str] = None
    language_other: Optional[str] = None
    is_primary_language: Optional[bool] = None
