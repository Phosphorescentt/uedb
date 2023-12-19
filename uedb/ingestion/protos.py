from uedb.errors import UEDBNotFoundError
from result import Result
from typing import Protocol

from db.model.university import University
from db.model.team import Team
from db.model.tournament import Tournament


class Ingester(Protocol):
    def get_university(self) -> Result[University, UEDBNotFoundError]:
        ...

    def get_team(self) -> Result[Team, UEDBNotFoundError]:
        ...

    def get_tournament(self) -> Result[Tournament, UEDBNotFoundError]:
        ...
