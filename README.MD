
# Restaurant Reviews API

## Overview

A Flask version of the API for the [Restaurant Reviews app](https://github.com/tdnelson2/mws-restaurant-review-app).

### Requirements

In a Linux environment install the following:
```
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install postgresql
sudo apt-get -qqy install python python-pip
sudo pip2 install --upgrade pip
sudo pip2 install flask packaging oauth2client redis passlib flask-httpauth
sudo pip2 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests
sudo pip install -U flask-cors
```
### Database setup

* In a Linux environment `cd` to `/var/www/html`.
* Login to PostgreSQL:
```
sudo -u postgres psql
```

* Create the database:
```
\i create_db.sql;
\q
```

* Create the database model and populate it:
```
sudo python database_setup.py
sudo python data_importer.py
```

### API Setup
* In a Linux environment `cd` to `/var/www/html`.
* Run `sudo git clone https://github.com/tdnelson2/mws-restaurant-reviews-api-flask.git restaurant-reviews-api`
* `sudo nano /etc/apache2/sites-available/default-ssl.conf` add the following inside `<VirtualHost _default_:443>`:
```
    WSGIDaemonProcess restaurant-reviews-api user=student group=student threads=5 python-home=/var/www/html/restaurant-reviews-api:/var/www/html/restaurant-reviews-api/env/lib/python2.7/site-packages
    WSGIScriptAlias /restaurant-reviews-api /var/www/html/restaurant-reviews-api/myapp_init.wsgi
    <Directory /var/www/html/restaurant-reviews-api>
        WSGIApplicationGroup restaurant-reviews-api
        WSGIProcessGroup restaurant-reviews-api
        Order deny,allow
        Allow from all
    </Directory>
```
* Restart Apache:
```
sudo apache2ctl restart
```
* API should now by setup!

## Endpoints

### GET Endpoints

#### Get all restaurants
```
/restaurants/
```

#### Get a restaurant by id
```
/restaurants/<restaurant_id>
```

#### Get all reviews for a restaurant
```
/reviews/?restaurant_id=<restaurant_id>
```

#### Get a restaurant review by id
```
/reviews/<review_id>
```
