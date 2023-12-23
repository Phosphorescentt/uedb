from result import is_err, is_ok
from uedb.errors import IngesterNotFoundError, TournamentOrganiserNotFound
from uedb.enums import TournamentOrganiser
from fastapi import APIRouter
from ingestion.utils import get_ingester_from_url
from pydantic import BaseModel, Field, field_validator


class UniversityIngest(BaseModel):
    url: str = Field(
        pattern="(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    )

    @field_validator("url", mode="after")
    @classmethod
    def check_to_name_present(cls, v):
        # TODO: Fix this - it's a bit hacky and not ideal. We shouldn't really be
        # using the TournamentOrganiser enum for this I don't think lol

        # Also this still causes us to error out and send a 500 back to the user which
        # is not what we want. We want to send a detailed validation error back
        # but I'm not sure how to do that yet :(
        if any([t.value.lower() in v for t in TournamentOrganiser]):
            return v
        else:
            raise TournamentOrganiserNotFound(v)


router = APIRouter(prefix="/universities")


@router.post("")
def ingest_university(query: UniversityIngest):
    """Ingest a university into the database based on their homepage URL on either the
    NUEL or NSE websites."""
    ingester = get_ingester_from_url(query.url)
    if ingester:
        university = ingester.get_university_by_url()
        if is_ok(university):
            return university
        elif is_err(university):
            return f"Unable to find university for URL {query.url}"
    else:
        raise IngesterNotFoundError(query.url)
