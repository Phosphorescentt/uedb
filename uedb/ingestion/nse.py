from result import Err, Result

from core.errors import ScrapingUniversityNotFoundError
from db.model.university import University

from .protocols import Ingester

# Not working on NSE ingestion right now.
# class NSEIngester(Ingester):
#     @staticmethod
#     def get_university_by_url(
#         url: str,
#     ) -> Result[University, ScrapingUniversityNotFoundError]:
#         return Err(ScrapingUniversityNotFoundError())
