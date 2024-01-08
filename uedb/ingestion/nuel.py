import requests
from db.model.university import University
from result import Err, Ok, Result

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
        university_response = requests.get(
            self.INSTITUTION_ROOT.format(university_name)
        )
        university_raw = university_response.json()

        print(university_raw)
        if university_raw.get("status") == "success":
            return Ok(university_raw.get("returnData"))

        return Err(APINotFoundError())
