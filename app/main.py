from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/caretakers/", response_model=schemas.Caretaker)
def create_caretaker(caretaker: schemas.CaretakerCreate, db: Session = Depends(get_db)):
    return crud.create_caretaker(db=db, caretaker=caretaker)

@app.get("/caretakers/", response_model=list[schemas.Caretaker])
def read_caretakers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    caretakers = crud.get_caretakers(db, skip=skip, limit=limit)
    return caretakers

@app.get("/caretakers/{caretaker_id}", response_model=schemas.Caretaker)
def read_caretaker(caretaker_id: int, db: Session = Depends(get_db)):
    db_caretaker = crud.get_caretaker(db, caretaker_id=caretaker_id)
    return db_caretaker

@app.post("/animals/{caretaker_id}", response_model=schemas.Animal)
def create_animal_for_caretaker(caretaker_id: int,animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.create_animal(db=db, animal=animal,caretaker_id=caretaker_id)


@app.get("/animals/", response_model=list[schemas.Animal])
def read_animals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    animals = crud.get_animals(db, skip=skip, limit=limit)
    return animals


@app.get("/animals/{animal_id}", response_model=schemas.Animal)
def read_animal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = crud.get_animal(db, animal_id=animal_id)
    return db_animal


@app.post("/toys/{animal_id}", response_model=schemas.Toy)
def create_toy_for_animal(animal_id: int, toy: schemas.ToyCreate, db: Session = Depends(get_db)):
    return crud.create_animal_toy(db=db, toy=toy, animal_id=animal_id)


@app.get("/toys/", response_model=list[schemas.Toy])
def read_toys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    toys = crud.get_toys(db, skip=skip, limit=limit)
    return toys
