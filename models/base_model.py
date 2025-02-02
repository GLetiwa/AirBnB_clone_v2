#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    # question 6 block
    id = Column(String(60), nullable=False, unique=True, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    # endof q6 block

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        # new dict block
        base_attributes = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
            }

        # end of dict block
        if not kwargs:

            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self) moved according to question 6
            self.save()
        # new elif block
        elif (set(base_attributes.keys()).issubset(kwargs.keys()) is False):

            if '__class__' in kwargs.keys():
                del kwargs['__class__']

            for attrib in base_attributes:
                if attrib not in kwargs.keys():
                    kwargs[attrib] = base_attributes[attrib]
            self.__dict__.update(kwargs)
            # storage.new(self) moved according to question 6
            self.save()
        # end of elif block
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)  # moved from init(q6)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)

        # The below nonsense returns the classname
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})

        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        # delete the key _sa_instance_state if it exists
        if ('_sa_instance_state' in dictionary.keys()):
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        from models import storage
        storage.delete(self)
