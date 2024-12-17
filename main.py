from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional
import sqlite3
from sqlmodel import Field, SQLModel, create_engine, Session, select


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


class Afspraken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titel: str
    dag: dag
    maand: maand
    jaar: jaar


engine = create_engine("sqlite:///afspraken.db")

app = FastAPI()

with sqlite3.connect("afspraken.db") as connection:
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS afspraken (id INTEGER PRIMARY KEY, titel TEXT, dag INTEGER, maand TEXT, jaar INTEGER)"
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
    async def create_afspraak(afspraak: Afspraken):
        with Session(engine) as session:
            session.add(afspraak)
            session.commit()
        return {"message": "Afspraak toegevoegd"}

    @app.delete("/{titel}")
    async def delete_afspraak(titel: str):
        with Session(engine) as session:
            statement = select(Afspraken).where(Afspraken.titel == titel)
            results = session.exec(statement)
            afspraak = results.one()
            session.delete(afspraak)
            session.commit()
        return {"message": "Afspraak verwijderd"}

    @app.get("/")
    async def root():
        with Session(engine) as session:
            afspraken = session.exec(select(Afspraken)).all()
        return afspraken
