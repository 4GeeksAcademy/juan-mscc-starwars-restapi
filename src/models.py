from typing import List


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    
    fav_chars: Mapped[List["FavChar"]] = relationship(back_populates="user")
    fav_planets: Mapped[List["FavPlanet"]] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email
        }

class Character(db.Model):

    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    species: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(String(120), nullable=False)

    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    origin_planet: Mapped["Planet"] = relationship(back_populates="characters")
    

    fav_chars: Mapped[List["FavChar"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "planet": self.origin_planet.name
        }

class Planet(db.Model):

    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    system: Mapped[str] = mapped_column(String(120), nullable=False)
    suns: Mapped[int] = mapped_column(nullable=False)
    

    characters: Mapped[List["Character"]] = relationship(back_populates="origin_planet")
    fav_planets: Mapped[List["FavPlanet"]] = relationship(back_populates="planet")

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "system": self.system,
            "suns": self.suns
        }

class FavChar(db.Model):

    __tablename__ = "fav_char"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    id_char: Mapped[int] = mapped_column(ForeignKey("character.id"))
    date: Mapped[str] = mapped_column(String(120), nullable=False)
    

    user: Mapped["User"] = relationship(back_populates="fav_chars")
    character: Mapped["Character"] = relationship(back_populates="fav_chars")


    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
        }

class FavPlanet(db.Model):

    __tablename__ = "fav_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    id_planet: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    date: Mapped[str] = mapped_column(String(120), nullable=False)
    

    user: Mapped["User"] = relationship(back_populates="fav_planets")
    planet: Mapped["Planet"] = relationship(back_populates="fav_planets")

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
        }
