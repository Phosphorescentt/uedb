from typing import Protocol

from core.errors import UEDBNotFoundError
from db.model.university import University
from result import Result


class Ingester(Protocol):
    @staticmethod
    def get_university_by_url(url: str) -> Result[University, Exception]:
        ...
