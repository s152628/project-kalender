from pydantic import BaseModel, ValidationError, AfterValidator
from typing import Annotated, Optional


def validate_straatnaam(value: str):
    if not value.strip():
        raise ValueError("Straatnaam mag niet leeg zijn.")
    return value


def validate_huisnummer(value: int):
    if value <= 0:
        raise ValueError("Huisnummer moet groter dan 0 zijn.")
    return value


def validate_postbus(value: int):
    if value <= 0:
        raise ValueError("Postbus moet groter dan 0 zijn.")
    return value


def validate_postcode(value: int):
    if not (1000 <= value <= 9992):
        raise ValueError("Postcode moet tussen 1000 en 9992 liggen.")
    return value


def validate_gemeente(value: str):
    if not value.strip():
        raise ValueError("Gemeente mag niet leeg zijn.")
    return value


straatnaam = Annotated[str, AfterValidator(validate_straatnaam)]
huisnummer = Annotated[int, AfterValidator(validate_huisnummer)]
postbus = Annotated[Optional[int], AfterValidator(validate_postbus)]
postcode = Annotated[int, AfterValidator(validate_postcode)]
gemeente = Annotated[str, AfterValidator(validate_gemeente)]


class Adres(BaseModel):
    straatnaam: straatnaam
    huisnummer: huisnummer
    postbus: postbus = None
    postcode: postcode
    gemeente: gemeente


class Student(BaseModel):
    studentennummer: int
    geboortedatum: str
    adres: Adres


studentenlijst = []


while True:
    print("\nVul de gegevens van de student in (of type 'stop' om te stoppen):")

    try:
        studentennummer = input("Studentennummer: ")
        if studentennummer.lower() == "stop":
            break

        geboortedatum = input("Geboortedatum (dd/mm/jjjj): ")

        print("\nAdresgegevens:")
        straatnaam = input("Straatnaam: ")
        huisnummer = input("Huisnummer: ")
        postbus = input("Postbus (optioneel): ") or None
        postcode = input("Postcode: ")
        gemeente = input("Gemeente: ")

        adres = Adres(
            straatnaam=straatnaam,
            huisnummer=int(huisnummer),
            postbus=int(postbus) if postbus else None,
            postcode=int(postcode),
            gemeente=gemeente,
        )

        student = Student(
            studentennummer=int(studentennummer),
            geboortedatum=geboortedatum,
            adres=adres,
        )

        studentenlijst.append(student)
        print(f"\nStudent geregistreerd: {student}")

    except ValidationError as e:
        print("\nEr is een fout opgetreden bij de registratie:")
        print(e)
    except ValueError as e:
        print("\nOngeldige invoer:")
        print(e)


print("\nGeregistreerde studenten:")
for student in studentenlijst:
    print(student)
