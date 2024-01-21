from typing import Optional

from core.enums import TournamentOrganiser
from fastapi import APIRouter
from ingestion.utils import get_ingester_from_url
from pydantic import BaseModel, Field, field_validator
from result import Err, Ok, Result, is_err, is_ok


class UniversityIngest(BaseModel):
    url: str = Field(
        pattern="(http(s)?:\\/\\/.)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)"
    )

    @field_validator("url", mode="after")
    @classmethod
    def check_to_name_present(cls, v) -> Optional[str]:
        # TODO: Fix this - it's a bit hacky and not ideal. We shouldn't really be
        # using the TournamentOrganiser enum for this I don't think lol

        # Also this still causes us to error out and send a 500 back to the user which
        # is not what we want. We want to send a detailed validation error back
        # but I'm not sure how to do that yet :(
        if any([t.value.lower() in v for t in TournamentOrganiser]):
            return v
        else:
            return None


router = APIRouter(prefix="/universities")


@router.post("")
def ingest_university(query: UniversityIngest):
    """Ingest a university into the database based on their homepage URL on either the
    NUEL or NSE websites."""
    if isinstance(query.url, Err):
        return "Tournament oragniser not found for URL."

    if not query.url:
        return "Unable to find Tournament organiser."

    university_url = query.url
    ingester_result = get_ingester_from_url(university_url)
    if isinstance(ingester_result, Err):
        return f"Unable to find ingester for ULR {university_url}"

    ingester = ingester_result.ok_value
    university_result = ingester.get_university_by_url(university_url)
    if is_ok(university_result):
        return university_result.ok_value
    elif is_err(university_result):
        return f"Unable to find university for URL {university_url}"
