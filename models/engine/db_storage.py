#!/usr/bin/python3
"""db storage module"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage(BaseModel):
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
        Base.metadata.create_all(self.__engine)
        self.__session = Session(self.__engine)
        lists = []
        objects = {}
        if not cls:
            lists.append(self.__session.query(State).all())
            lists.append(self.__session.query(City).all())
            lists.appned(self.__session.query(User).all())
            lists.append(self.__session.query(Amenity).all())
            lists.append(self.__session.query(Review).all())
            lists.append(self.__session.query(Place).all())
            for elem in lists:
                objects.update(elem.__class__.__name__ + elem.id: elem)
        else:
            for elem in self.__session.query(cls):
                objects.update(elem.__class__.__name__ + elem.id: elem)
        return (objects)

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
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
        session_factory = sessionmaker(
                                        bind=some_engine,
                                        expire_on_commit=False
                                        )
        Session = scoped_session(session_factory)
        self.__session = Session()
