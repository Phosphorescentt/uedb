from typing import Protocol

from db.model.university import University
from result import Result


class Ingester(Protocol):
    @staticmethod
    def get_university_by_url(url: str) -> Result[University, Exception]:
        ...
