from typing import Optional

from ingestion.nse import NSEIngester
from ingestion.nuel import NUELIngester
from ingestion.protos import Ingester


def get_ingester_from_url(url: str) -> Optional[Ingester]:
    urll = url.lower()
    if "nuel" in urll:
        return NUELIngester()
    elif "nse" in urll:
        return NSEIngester()

    return None
