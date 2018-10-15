
const fs           = require('fs');
const util         = require('util');
const readFile     = util.promisify(fs.readFile);
const writeFile     = util.promisify(fs.writeFile);

readFile('./originalData.json', 'utf8')
  .then(contents => {
    const originalData = JSON.parse(contents);
    const restaurants = originalData.data.restaurants;
    const reviews = originalData.data.reviews;
    for (const restaurant of restaurants) {
      const createdAt = new Date(restaurant.createdAt);
      const updatedAt = new Date(restaurant.updatedAt);
      restaurant.createdAt = createdAt.toISOString();
      restaurant.updatedAt = updatedAt.toISOString();
    }
    for (const review of reviews) {
      const createdAt = new Date(review.createdAt);
      const updatedAt = new Date(review.updatedAt);
      review.createdAt = createdAt.toISOString();
      review.updatedAt = updatedAt.toISOString();
    }
    const r1 = writeFile('./restaurants.json', JSON.stringify(restaurants, null, 2), 'utf8');
    const r2 = writeFile('./reviews.json', JSON.stringify(reviews, null, 2), 'utf8');
    return Promise.all([r1, r2]);
  })
  .then(() => console.log('timecodes updated!'))
  .catch(err => console.log(err));