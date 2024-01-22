from result import Err, Ok, Result

from core.enums import TournamentOrganiser
from core.errors import IngesterNotFoundError
from ingestion.nuel import NUELIngester
from ingestion.protocols import Ingester


def get_ingester_from_url(url: str) -> Result[Ingester, IngesterNotFoundError]:
    urll = url.lower()
    if "nuel" in urll:
        return Ok(NUELIngester())
    # Not working on NSE ingestion right now.
    # elif "nse" in urll:
    #     return Ok(NSEIngester())

    return Err(IngesterNotFoundError())


def check_to_in_string(s: str) -> bool:
    # TODO: Fix this - it's a bit hacky and not ideal. We shouldn't really be
    # using the TournamentOrganiser enum for this I don't think lol
    if any([t.value.lower() in s.lower() for t in TournamentOrganiser]):
        return True
    else:
        return False
