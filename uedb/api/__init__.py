from api.ingest import ingestion_router
from api.rest import rest_router
from api.query import query_router
from api.management import management_router

fast_api_routers = [ingestion_router, rest_router, query_router, management_router]
