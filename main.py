from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator
from typing import Annotated
import sqlite3


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


def jaar_validator(jaar: int):
    if jaar < 2024:
        raise ValueError("Jaar moet 2024 of later zijn.")
    return jaar


dag = Annotated[int, AfterValidator(dag_validator)]
maand = Annotated[
    str,
    AfterValidator(maand_validator),
]
jaar = Annotated[int, AfterValidator(jaar_validator)]


class Afspraak(BaseModel):
    titel: str
    dag: dag
    maand: maand
    jaar: jaar


app = FastAPI()

with sqlite3.connect("afspraken.db") as connection:
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS afspraken (titel TEXT, dag INTEGER, maand TEXT, jaar INTEGER)"
    )
    res = cursor.execute("SELECT * FROM afspraken")
    if not res.fetchall():
        cursor.execute(
            """INSERT INTO afspraken (titel, dag, maand, jaar) VALUES
            ("dokter afspraak", 12, "mei", 2025),
            ("tandarts afspraak", 15, "mei", 2025),
            ("kapper afspraak", 18, "mei", 2025)"""
        )
        connection.commit()

    @app.post("/")
    async def create_afspraak(afspraak: Afspraak):
        cursor.execute(
            "INSERT INTO afspraken (titel, dag, maand, jaar) VALUES (?, ?, ?, ?)",
            (afspraak.titel, afspraak.dag, afspraak.maand, afspraak.jaar),
        )
        connection.commit()
        return {"message": "Afspraak toegevoegd"}

    @app.delete("/{titel}")
    async def delete_afspraak(titel: str):
        cursor.execute("DELETE FROM afspraken WHERE titel = ?", (titel,))
        connection.commit()
        return {"message": "Afspraak verwijderd"}

    @app.get("/")
    async def root():
        res = cursor.execute("SELECT * FROM afspraken")
        return res.fetchall()
