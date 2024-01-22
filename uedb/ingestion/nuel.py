from typing import Any, Dict, Union

import requests
from result import Err, Ok, Result
from sqlmodel import select

from core.enums import TournamentOrganiser
from core.errors import APINotFoundError, ParsingError
from db.model.grouped_university import GroupedUniversity
from db.model.team import Team
from db.model.university import University
from db.utils import get_session_context_manager

from .protocols import Ingester


class NUELParser:
    @staticmethod
    def university_response_to_db_model(
        url: str,
        json: Dict[str, Any],
    ) -> Result[University, ParsingError]:
        try:
            with get_session_context_manager() as session:
                grouped_universities = GroupedUniversity.search(json["name"], session)

            return Ok(
                University(
                    url=url,
                    name=json["name"],
                    tournament_organiser=TournamentOrganiser.NUEL,
                    tournament_organiser_identifier=json["_id"],
                    grouped_university_id=grouped_universities[0].id
                    if len(grouped_universities) == 1
                    else None,
                )
            )
        except KeyError as e:
            return Err(ParsingError(e))

    @staticmethod
    def team_response_to_db_model(
        json: Dict[str, Any],
    ) -> Result[Team, ParsingError]:
        try:
            with get_session_context_manager() as session:
                universities = session.exec(
                    select(University).where(
                        University.tournament_organiser_identifier
                        == json.get("equipo", {}).get("institution", {}).get("id")
                    )
                ).all()

            if len(universities) != 1:
                raise ParsingError("Could not match team to university")
            else:
                university_id = id if (id := universities[0].id) else None

            if not (university_id := universities[0].id):
                raise ParsingError("Could not get university's id")

            return Ok(
                Team(
                    name=json["equipo"]["name"],
                    university_id=university_id,
                    tournament_organiser_slug=json["equipo"]["slug"],
                    tournament_organiser_id=json["equipo"]["_id"],
                )
            )

        except KeyError as e:
            return Err(ParsingError(e))


class NUELIngester(Ingester):
    INSTITUTION_ROOT = (
        "https://api.thenuel.com/api/v001/showcase/university-esports/institution/{}"
    )
    TEAM_ROOT = "https://api.thenuel.com/api/v001/showcase/university-esports/equipo/{}"

    @staticmethod
    def get_university_by_url(
        url: str,
    ) -> Result[University, Union[APINotFoundError, ParsingError]]:
        university_name = url.split("/")[-1]
        university_response = requests.get(
            NUELIngester.INSTITUTION_ROOT.format(university_name)
        )
        university_raw = university_response.json()

        if not university_raw.get("status") == "success":
            return Err(APINotFoundError())

        return NUELParser.university_response_to_db_model(
            url, university_raw.get("returnData")
        )

    @staticmethod
    def get_team_by_url(
        url: str,
    ) -> Result[Team, Union[APINotFoundError, ParsingError]]:
        team_name = url.split("/")[-1]
        team_response = requests.get(NUELIngester.TEAM_ROOT.format(team_name))
        team_raw = team_response.json()

        if not team_raw.get("status") == "success":
            return Err(APINotFoundError())

        return NUELParser.team_response_to_db_model(team_raw.get("returnData"))
