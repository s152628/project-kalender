from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator
from typing import Annotated


def dag_validator(dag: int):
    if dag < 1 or dag > 31:
        raise ValueError("Dag moet tussen 1 en 31 liggen.")
    return dag


def maand_validator(maand: str):
    if maand not in [
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december",
    ]:
        raise ValueError(
            "Maand moet een van de volgende zijn: januari, februari, maart, april, mei, juni, juli, augustus, september, oktober, november, december."
        )
    return maand


dag = Annotated[int, AfterValidator(dag_validator)]
maand = Annotated[
    str,
    AfterValidator(maand_validator),
]


class Afspraak(BaseModel):
    titel: str
    dag: dag
    maand: maand
    jaar: int


afspraken = [
    {"titel": "dokter afspraak", "dag": 12, "maand": "mei", "jaar": 2025},
    {"titel": "tandarts afspraak", "dag": 15, "maand": "mei", "jaar": 2025},
    {"titel": "kapper afspraak", "dag": 18, "maand": "mei", "jaar": 2025},
]
app = FastAPI()


@app.post("/")
async def create_afspraak(afspraak: Afspraak):
    afspraken.append(afspraak)
    return afspraak


@app.delete("/{titel}")
async def delete_afspraak(titel: str):
    for i in range(len(afspraken)):
        if afspraken[i]["titel"] == titel:
            afspraken.pop(i)
            return {"message": "Afspraak verwijderd"}


@app.get("/")
async def root():
    return afspraken
