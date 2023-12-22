#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""


    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())


    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if len(kwargs) > 0:
            if 'id' not in kwargs.keys():
                self.__setattr__('id', str(uuid.uuid4()))
            if 'created_at' or 'updated_at' not in kwargs.keys():
                self.created_at = self.updated_at = datetime.now()
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    self.__setattr__(k, datetime.fromisoformat(v))
                elif k != '__class__':
                    self.__setattr__(k, v)


        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        from models import storage
        storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': self.__class__.__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # del dictionary['_sa_instance_state']
        return dictionary
    
    def delete(self):
        """Delete current instance from the storage"""
        from models import storage
        
        storage.delete(self)
