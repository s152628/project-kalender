from pydantic import BaseModel, AfterValidator, ValidationError
from typing import Annotated


def validate_age(value):
    if value <= 0 or value >= 125:
        raise ValueError("you must be between 0 and 125 years old")
    return value


Age = Annotated[int, AfterValidator(validate_age)]


class person(BaseModel):
    name: str
    age: Age


try:
    print(person(name="John", age=130))
except ValidationError as e:
    print(e)
