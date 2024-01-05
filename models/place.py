#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy import Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity
from models.review import Review

place_amenity = Table(
            "place_amenity",
            Base.metadata,
            Column("place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False
                ),
            Column("amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False
                ),
        )

class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                cascade="all, delete")
        amenities = relationship(
            "Amenity", secondary=place_amenity,
            back_populates="places", viewonly=False
        )
    else:
        @property
        def reviews(self):
            """Returns the list of Review instances with
            place_id equals to the current Place.id"""
            from models import storage
            reviews = storage.all(Review)
            reviews_instances = []
            for key, value in reviews.items():
                if value.place_id == self.id:
                    reviews_instances.append(value)
            return reviews_instances

        @property
        def amenities(self):
            """eturns the list of Amenity instances based on
            the attribute amenity_ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """handles append method for adding an Amenity.id
            to the attribute amenity_ids"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
