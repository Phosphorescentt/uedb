class UEDBNotFoundError(Exception):
    """Generic error to be raise if we can't find ingest the data from somewhere."""

    ...


class ScrapingNotFoundError(UEDBNotFoundError):
    """Generic error type to be raised if something goes wrong scraping data from a web page."""

    ...


class ScrapingUniversityNotFoundError(ScrapingNotFoundError):
    """Raised if a university cannot be found via scraping"""

    ...


class APINotFoundError(UEDBNotFoundError):
    """Raised if an API call can't find the requested resource."""

    ...


class IngesterNotFoundError(UEDBNotFoundError):
    """Raised if we cannot find an ingester for the URL provided.

    In theory, this should never get raised as this should get caught during
    validation, but better safe than sorry!"""


class TournamentOrganiserNotFound(UEDBNotFoundError):
    """Raise if we don't recognise the URL that the user has submitted for ingestion
    as a URL belonging to one of the tournament organisers."""
