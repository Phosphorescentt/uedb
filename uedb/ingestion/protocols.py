from typing import Protocol

from result import Result

from db.model.team import Team
from db.model.university import University


class Ingester(Protocol):
    @staticmethod
    def get_university_by_url(url: str) -> Result[University, Exception]:
        ...

    @staticmethod
    def get_team_by_url(url: str) -> Result[Team, Exception]:
        ...
