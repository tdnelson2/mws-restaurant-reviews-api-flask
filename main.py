from flask import Flask, render_template, request, redirect
from flask_cors import CORS

import json

from my_path_data import root_url
from my_path_data import html_index_root


app = Flask(__name__)
CORS(app)
app.secret_key = 'super_secret_key'

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import (Base,
                            Neighborhood,
                            CuisineType,
                            Restaurant,
                            Review)

engine = create_engine('postgresql://student:password@localhost/mydb')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

##########################################################
"""
ROUTES
"""
##########################################################

@app.route(root_url+'/restaurants')
def restaurants():
    r = getRestaurants()
    data = [entry.serialize for entry in r]
    return json.dumps(data)
session = DBSession()

@app.route(root_url+'/restaurants/<int:restaurant_id>/')
def restaurant(restaurant_id):
    data = None
    try:
        data = getRestaurant(restaurant_id).serialize
    except:
        print('id does not exist')
        return json.dumps([])
    if data:
        return json.dumps(data)

@app.route(root_url+'/reviews/')
def reviews():
    restaurant_id = request.args.get('restaurant_id')
    review_id = request.args.get('review_id')
    data = []
    if restaurant_id:
        try:
            r = getReviewsForRestaurant(restaurant_id)
            data = [entry.serialize for entry in r]
        except:
            print('restaurant_id not found')
    elif review_id:
        try:
            data = getReview(review_id).serialize
        except:
            print('review_id not found')
    if data:
        return json.dumps(data)

##########################################################
"""
DATABASE FUNCTIONS
"""
##########################################################

def getRestaurant(id):
    return session.query(Restaurant).filter_by(id=int(id)).one()

def getRestaurants():
    return session.query(Restaurant).order_by(asc(Restaurant.id))

def getReviewsForRestaurant(id):
    return session.query(Review).filter_by(restaurant_id=int(id))\
        .order_by(asc(Review.createdAt))

def getReview(id):
    return session.query(Review).filter_by(id=int(id)).one()

##########################################################

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=1336)