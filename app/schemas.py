from pydantic import BaseModel


class ToyBase(BaseModel):
    title: str
    description: str | None = None


class ToyCreate(ToyBase):
    pass


class Toy(ToyBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class AnimalBase(BaseModel):
    name: str
    gender: str


class AnimalCreate(AnimalBase):
    pass


class Animal(AnimalBase):
    fact: str
    id: int
    caretaker_id: int
    toys: list[Toy] = []

    class Config:
        orm_mode = True


class CaretakerBase(BaseModel):
    email: str


class CaretakerCreate(CaretakerBase):
    password: str


class Caretaker(CaretakerBase):
    id: int
    animals: list[Animal] = []

    class Config:
        orm_mode = True
