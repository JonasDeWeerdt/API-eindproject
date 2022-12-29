from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Caretaker(Base):
    __tablename__ = "caretakers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    animals = relationship("Animal", back_populates="caretakers")


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String)
    fact = Column(String)
    hashed_name = Column(String)
    caretaker_id = Column(Integer, ForeignKey("caretakers.id"))

    toys = relationship("Toy", back_populates="owner")
    caretakers = relationship("Caretaker", back_populates="animals")


class Toy(Base):
    __tablename__ = "toys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("animals.id"))

    owner = relationship("Animal", back_populates="toys")
