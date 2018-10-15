import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import (Base,
                            Neighborhood,
                            CuisineType,
                            Restaurant,
                            Review)

from my_path_data import db_login

restaurant_data = json.loads(open('./data/restaurants.json').read())
review_data = json.loads(open('./data/reviews.json').read())

engine = create_engine(db_login)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


neighborhoods = []
cuisines = []
for r in restaurant_data:
  if not r['neighborhood'] in neighborhoods:
    neighborhoods.append(r['neighborhood'])
  if not r['cuisine_type'] in cuisines:
    cuisines.append(r['cuisine_type'])

# Create neighborhoods

for neighborhood in neighborhoods:
    neighborhood_category = Neighborhood(name=neighborhood)

    session.add(neighborhood_category)
    session.commit()


print "\n\nneighborhoods!\n\n"

# Create cuisine types

for cuisine in cuisines:
    cuisine_category = CuisineType(name=cuisine)

    session.add(cuisine_category)
    session.commit()


print "\n\ncuisines added!\n\n"

# Create restaurants

for r in restaurant_data:
  neighborhood = session.query(Neighborhood)\
    .filter_by(name=r['neighborhood']).one()
  cuisine_type = session.query(CuisineType)\
    .filter_by(name=r['cuisine_type']).one()
  restaurant = Restaurant(id=int(r['id']),
                          name=r['name'],
                          neighborhood=neighborhood.id,
                          photograph=r['photograph'],
                          address=r['address'],
                          latlng=json.dumps(r['latlng']),
                          cuisine_type=cuisine_type.id,
                          operating_hours=json.dumps(r['operating_hours']),
                          createdAt=str(r['createdAt']),
                          updatedAt=str(r['updatedAt']),
                          is_favorite=str(r['is_favorite']))

  session.add(restaurant)
  session.commit()


print "\n\nrestaurants added!\n\n"

# Create reviews

for r in review_data:
  review = Review(id=r['id'],
                  restaurant_id=int(r['restaurant_id']),
                  name=r['name'],
                  createdAt=str(r['createdAt']),
                  updatedAt=str(r['updatedAt']),
                  rating=int(r['rating']),
                  comments=r['comments'])

  session.add(review)
  session.commit()


print "\n\nreviews added!\n\n"

