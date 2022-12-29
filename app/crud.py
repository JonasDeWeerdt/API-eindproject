import json
from sqlalchemy.orm import Session
import requests
import auth
import models
import schemas


def get_animal(db: Session, animal_id: int):
    return db.query(models.Animal).filter(models.Animal.id == animal_id).first()


def get_animal_by_name(db: Session, name: str):
    return db.query(models.Animal).filter(models.Animal.name == name).all()


def get_animals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Animal).offset(skip).limit(limit).all()


def create_animal(db: Session, animal: schemas.AnimalCreate,caretaker_id:int):
    hashed_name = auth.get_hash(animal.name)
    if animal.name.lower() == "cat":
        response = requests.get('https://catfact.ninja/fact')
        db_animal = models.Animal(name=animal.name, gender=animal.gender, hashed_name=hashed_name,caretaker_id=caretaker_id, fact=json.loads(response.text)["fact"])
    else:
        db_animal = models.Animal(name=animal.name, gender=animal.gender, hashed_name=hashed_name,caretaker_id=caretaker_id, fact="non-cat")
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def get_toys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Toy).offset(skip).limit(limit).all()


def create_animal_toy(db: Session, toy: schemas.ToyCreate, animal_id: int):
    db_toy = models.Toy(**toy.dict(), owner_id=animal_id)
    db.add(db_toy)
    db.commit()
    db.refresh(db_toy)
    return db_toy


def get_caretaker(db: Session, caretaker_id: int):
    return db.query(models.Caretaker).filter(models.Caretaker.id == caretaker_id).first()


def get_caretaker_by_email(db: Session, email: str):
    return db.query(models.Caretaker).filter(models.Caretaker.name == email).first()


def get_caretakers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Caretaker).offset(skip).limit(limit).all()


def create_caretaker(db: Session, caretaker: schemas.CaretakerCreate):
    hashed_string = auth.get_hash(caretaker.password)
    db_caretaker = models.Caretaker(email=caretaker.email, password=hashed_string)
    db.add(db_caretaker)
    db.commit()
    db.refresh(db_caretaker)
    return db_caretaker
