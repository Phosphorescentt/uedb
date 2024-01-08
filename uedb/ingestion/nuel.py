import requests
from result import Result, Err
from db.model.university import University
from uedb.errors import APINotFoundError
from .protos import Ingester


class NUELIngester(Ingester):
    INSTITUTION_ROOT = (
        "https://api.thenuel.com/api/v001/showcase/university-esports/institution/{}"
    )

    def get_university_by_url(
        self,
        url: str,
    ) -> Result[University, APINotFoundError]:
        university_name = url.split("/")[-1]
        university_raw = requests.get(self.INSTITUTION_ROOT.format(university_name))
        print(university_raw.json())

        return Err(APINotFoundError())
