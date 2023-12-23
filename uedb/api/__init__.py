from api.ingest import ingestion_router
from api.query import query_router

fast_api_routers = [ingestion_router, query_router]
