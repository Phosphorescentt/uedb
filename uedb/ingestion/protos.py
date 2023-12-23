from uedb.errors import UEDBNotFoundError
from result import Result
from typing import Protocol

from db.model.university import University


class Ingester(Protocol):
    def get_university_by_url(self) -> Result[University, UEDBNotFoundError]:
        ...
