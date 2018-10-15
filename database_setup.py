import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from my_path_data import db_login


engine = create_engine(db_login)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class Neighborhood(Base):
    """a table containing all possible neighborhoods"""
    __tablename__ = 'neighborhoods'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name' : self.name
        }


class CuisineType(Base):
    """a table containing all possible cuisine types"""
    __tablename__ = 'cuisine_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name' : self.name
        }

class Restaurant(Base):
    """a table containing all restaurants"""
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    neighborhood = Column(Integer, ForeignKey('neighborhoods.id'))
    photograph = Column(String(250))
    address = Column(String(250))
    latlng = Column(String(50))
    cuisine_type = Column(Integer, ForeignKey('cuisine_types.id'))
    operating_hours = Column(String(1000))
    createdAt = Column(String(100))
    updatedAt = Column(String(100))
    is_favorite = Column(String(5))
    neighborhood_category = relationship(Neighborhood)
    cuisine_type_category = relationship(CuisineType)

    @property
    def serialize(self):
        neighborhood = session.query(Neighborhood)\
        .filter_by(id=self.neighborhood).one()
        cuisine_type = session.query(CuisineType)\
        .filter_by(id=self.cuisine_type).one()
        return {
            'id' : self.id,
            'name' : self.name,
            'neighborhood' : neighborhood.name,
            'photograph' : self.photograph,
            'address' : self.address,
            'latlng' : json.loads(self.latlng),
            'cuisine_type' : cuisine_type.name,
            'operating_hours' : json.loads(self.operating_hours),
            'createdAt' : self.createdAt,
            'updatedAt' : self.updatedAt,
            'is_favorite' : self.is_favorite
        }

class Review(Base):
    """a table containing all reivews"""
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key = True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name =Column(String(80), nullable=False)
    createdAt = Column(String(100))
    updatedAt = Column(String(100))
    rating = Column(Integer)
    comments = Column(String(4000))
    restaurants = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'restaurant_id' : self.restaurant_id,
            'name' : self.name,
            'createdAt' : self.createdAt,
            'updatedAt' : self.updatedAt,
            'rating' : self.rating,
            'comments' : self.comments
        }

Base.metadata.create_all(engine)