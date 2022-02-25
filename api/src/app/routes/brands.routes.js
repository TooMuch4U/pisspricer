const brands = require('../controllers/brands.controller');
const itemPrices = require('../controllers/itemPrices.controller');
const items = require('../controllers/items.controller');
const authenticate = require('../middleware/authenticate');

module.exports = function(app) {
    const baseUrl = app.rootUrl + '/brands';

    app.route(baseUrl + '/')
        .get(brands.getAll)
        .post(authenticate.adminRequired, brands.insert);
    app.route(baseUrl + '/:brandId')
        .get(brands.getOne)
        .patch(authenticate.adminRequired, brands.update)
        .delete(authenticate.adminRequired, brands.delete)

    app.route(baseUrl + '/:brandId/fullitem')
        .put(authenticate.adminRequired, items.setItemAndPrice);

    app.route(baseUrl + '/:brandId/image')
        .put(authenticate.adminRequired, brands.setImage);
};
