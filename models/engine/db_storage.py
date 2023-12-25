#!/usr/bin/python3
"""db storage module"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Define DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Define a constructor for DBStorage"""
        dev_user = getenv('HBNB_MYSQL_USER')
        dev_pass = getenv('HBNB_MYSQL_PWD')
        dev_host = getenv('HBNB_MYSQL_HOST')
        dev_db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
                            'mysql+mysqldb://{}:{}@{}/{}'.format(
                                        dev_user, dev_pass, dev_host,
                                        dev_db), pool_pre_ping=True
                                    )

    def all(self, cls=None):
        """Return all instnaces of the cls"""
        classes = [State, City, User, Amenity, Review, Place]
        objects = {}
        if not cls:
            for cs in classes:
                instances = self.__session.query(cs).all()
                for instance in instances:
                    objects.update({instance.__class__.__name__ + instance.id: instance})
        else:
            instances = self.__session.query(cls).all()
            for elem in instances:
                objects.update({elem.__class__.__name__ + elem.id: elem})
        return (objects)

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False
                                       )
        Session = scoped_session(session_factory)
        self.__session = Session()
