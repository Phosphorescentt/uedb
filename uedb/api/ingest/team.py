from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator
from result import Err
from sqlmodel import Session

from uedb.core.errors import APINotFoundError, ParsingError
from uedb.db.utils import get_session
from uedb.ingestion.utils import check_to_in_string, get_ingester_from_url


class TeamIngest(BaseModel):
    url: str = Field(
        pattern="(http(s)?:\\/\\/.)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)"
    )

    @field_validator("url", mode="after")
    @classmethod
    def validate_url(cls, v) -> Optional[str]:
        if not check_to_in_string(v):
            return None

        if "team" not in v.lower():
            return None

        return v


router = APIRouter(prefix="/teams")


@router.post("")
def ingest_team(
    query: TeamIngest,
    session: Session = Depends(get_session),
):
    """Ingest a team into the database based on their URL on the either the NUEL or NSE
    webistes."""

    if not query.url:
        return "Unable to find tournament organiser."

    team_url = query.url
    ingester_result = get_ingester_from_url(team_url)
    if isinstance(ingester_result, Err):
        return f"Unable to find ingester for URL {team_url}"

    ingester = ingester_result.ok_value
    team_result = ingester.get_team_by_url(team_url)
    print(team_result)
    if isinstance(team_result, Err):
        if isinstance(team_result.err_value, APINotFoundError):
            return f"Unable to find team for URL {team_url}"
        elif isinstance(team_result.err_value, ParsingError):
            return "Unable to parse json into Team db object."
    else:
        team = team_result.ok_value
        session.add(team)
        session.commit()
        session.refresh(team)
        return team
