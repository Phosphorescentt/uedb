# The **U**niversity **E**sports **D**ata**b**ase (UEDB)

The University Esports Database is a [SQLModel](https://sqlmodel.tiangolo.com/) and [FastAPI](https://fastapi.tiangolo.com/) application to unify the UK University Esports universities and teams. The idea is that eventually, the application will be able to provide a data and metrics on universities and their performance in tournaments across both UK university tournament organisers ([NUEL](https://thenuel.com/) and [NSE](https://nse.gg/)).

# Setup

This project requires [Poetry](https://python-poetry.org/) for managing dependencies and runtimes. Run through the setup & installation of poetry before continuing here.

Once Poetry is installed, enter the root of the directory and run the following commands.

```bash
poetry install
poetry shell
cd uedb/
uvicorn main:app
```

This will start the application and you will be able to access the API documentation by going to `localhost:8000/docs`.
