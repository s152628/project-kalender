from fastapi import FastAPI
from pydantic import BaseModel


class Afspraak(BaseModel):
    titel: str
    dag: int
    maand: str
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
