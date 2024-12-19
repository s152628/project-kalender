from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, AfterValidator
from sqlmodel import Field, SQLModel, create_engine, Session, select
from passlib.context import CryptContext
import jwt
from typing import Optional, Generator, Annotated
from datetime import datetime, timedelta, timezone
import sqlite3


SECRET_KEY = "db5ad23006a5378b7a1437d4e06cfa9ad0460ee5a93fb0116eb100a37c740cc7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


DATABASE_URL = "sqlite:///afspraken.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    with sqlite3.connect("afspraken.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS afspraken (
                id INTEGER PRIMARY KEY, 
                titel TEXT, 
                dag INTEGER, 
                maand TEXT, 
                jaar INTEGER
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, 
                username TEXT, 
                password TEXT
            )
        """
        )

        if not cursor.execute("SELECT * FROM users").fetchone():
            cursor.execute(
                "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
                (1, "test", get_password_hash("test")),
            )
        if not cursor.execute("SELECT * FROM afspraken").fetchone():
            cursor.executemany(
                "INSERT INTO afspraken (id, titel, dag, maand, jaar) VALUES (?, ?, ?, ?, ?)",
                [
                    (1, "dokter afspraak", 12, "mei", 2025),
                    (2, "tandarts afspraak", 15, "mei", 2025),
                    (3, "kapper afspraak", 18, "mei", 2025),
                ],
            )
        connection.commit()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str


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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_user(session: Session, username: str) -> Optional[Users]:
    statement = select(Users).where(Users.username == username)
    return session.exec(statement).first()


def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = get_user(session, username)
        if user and verify_password(password, user.password):
            return user
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    with Session(engine) as session:
        user = get_user(session, username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user


app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@app.get("/")
async def read_afspraken(session: Session = Depends(get_session)):
    afspraken = session.exec(select(Afspraken)).all()
    return afspraken


@app.post("/")
async def create_afspraak(afspraak: Afspraken, session: Session = Depends(get_session)):
    session.add(afspraak)
    session.commit()
    return {"message": "Afspraak toegevoegd"}


@app.get("/{id}")
async def read_afspraak(id: int, session: Session = Depends(get_session)):
    afspraak = session.exec(select(Afspraken).where(Afspraken.id == id)).first()
    if not afspraak:
        raise HTTPException(status_code=404, detail="Afspraak niet gevonden")
    return afspraak


@app.delete("/{id}")
async def delete_afspraak(id: int, session: Session = Depends(get_session)):
    afspraak = session.exec(select(Afspraken).where(Afspraken.id == id)).first()
    if not afspraak:
        raise HTTPException(status_code=404, detail="Afspraak niet gevonden")
    session.delete(afspraak)
    session.commit()
    return {"message": "Afspraak verwijderd"}


init_db()
