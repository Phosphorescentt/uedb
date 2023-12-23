class UEDBNotFoundError(Exception):
    """Generic error to be raise if we can't find ingest the data from somewhere."""

    ...


class ScrapingNotFoundError(UEDBNotFoundError):
    """Generic error type to be raised if something goes wrong scraping data from a web page."""

    ...


class ScrapingUniversityNotFoundError(ScrapingNotFoundError):
    """Raised if a university cannot be found via scraping"""

    ...
