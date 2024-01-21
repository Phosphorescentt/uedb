from typing import Any, Dict, Union

import requests
from core.enums import TournamentOrganiser
from core.errors import APINotFoundError, UniversityParsingError
from db.model.grouped_university import GroupedUniversity
from db.model.university import University
from db.utils import get_session_context_manager
from fastapi import Depends
from result import Err, Ok, Result

from .protocols import Ingester


class NUELIngester(Ingester):
    INSTITUTION_ROOT = (
        "https://api.thenuel.com/api/v001/showcase/university-esports/institution/{}"
    )

    @staticmethod
    def _university_response_to_db_model(
        url: str,
        json: Dict[str, Any],
    ) -> Result[University, UniversityParsingError]:
        try:
            with get_session_context_manager() as session:
                grouped_universities = GroupedUniversity.search(json["name"], session)

            return Ok(
                University(
                    url=url,
                    name=json["name"],
                    tournament_organiser=TournamentOrganiser.NUEL,
                    grouped_university_id=grouped_universities[0].id
                    if len(grouped_universities) == 1
                    else None,
                )
            )
        except KeyError:
            return Err(UniversityParsingError())

    @staticmethod
    def get_university_by_url(
        url: str,
    ) -> Result[University, Union[APINotFoundError, UniversityParsingError]]:
        university_name = url.split("/")[-1]
        university_response = requests.get(
            NUELIngester.INSTITUTION_ROOT.format(university_name)
        )
        university_raw = university_response.json()

        print(university_raw)
        if not university_raw.get("status") == "success":
            return Err(APINotFoundError())

        return NUELIngester._university_response_to_db_model(
            url, university_raw.get("returnData")
        )
