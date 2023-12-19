# Generic error to be raise if we can't find ingest the data from somewhere.
class UEDBNotFoundError(Exception):
    ...


# Generic error type to be raised if something goes wrong scraping data from a web page.
class ScrapingNotFoundError(UEDBNotFoundError):
    ...


# Raised if a university cannot be found via scraping
class ScrapingUniversityNotFoundError(ScrapingNotFoundError):
    ...
