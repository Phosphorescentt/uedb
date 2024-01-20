from db.model.university import University
from result import Result, Err

from core.errors import ScrapingUniversityNotFoundError

from .protos import Ingester


class NSEIngester(Ingester):
    def get_university_by_url(
        self,
        url: str,
    ) -> Result[University, ScrapingUniversityNotFoundError]:
        return Err(ScrapingUniversityNotFoundError())
