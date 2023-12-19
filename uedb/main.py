from api import fast_api_routers
from db.utils import create_db_and_tables
from fastapi import FastAPI

app = FastAPI()
for router in fast_api_routers:
    app.include_router(router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
