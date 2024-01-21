from core.errors import IngesterNotFoundError
from ingestion.nse import NSEIngester
from ingestion.nuel import NUELIngester
from ingestion.protos import Ingester
from result import Err, Ok, Result


def get_ingester_from_url(url: str) -> Result[Ingester, IngesterNotFoundError]:
    urll = url.lower()
    if "nuel" in urll:
        return Ok(NUELIngester())
    elif "nse" in urll:
        return Ok(NSEIngester())

    return Err(IngesterNotFoundError())
