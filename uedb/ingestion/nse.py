from core.errors import ScrapingUniversityNotFoundError
from db.model.university import University
from result import Err, Result

from .protos import Ingester


class NSEIngester(Ingester):
    @staticmethod
    def get_university_by_url(
        url: str,
    ) -> Result[University, ScrapingUniversityNotFoundError]:
        return Err(ScrapingUniversityNotFoundError())
