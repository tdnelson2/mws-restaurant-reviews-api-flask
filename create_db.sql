
DROP DATABASE IF EXISTS restaurant_reviews;
CREATE ROLE student WITH LOGIN PASSWORD 'password';
CREATE DATABASE restaurant_reviews;
GRANT ALL PRIVILEGES on database restaurant_reviews to student;