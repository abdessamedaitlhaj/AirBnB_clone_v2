#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')

    else:

        @property
        def cities(self):
            """Returns list of City instances"""
            from models import storage
            cities = []
            for key, value in storage.all(City).items():
                if key.split('.')[1] == self.id:
                    cities.append(value)
            return (cities)
