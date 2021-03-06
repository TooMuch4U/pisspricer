const users = require('../controllers/users.controller');
const authenticate = require('../middleware/authenticate');

module.exports = function(app) {
    const baseUrl = app.rootUrl + '/users';

    app.route(baseUrl + '/register')
        .post(users.create);

    app.route(baseUrl + '/login')
        .post(users.login);

    app.route(baseUrl + '/logout')
        .post(authenticate.loginRequired, users.logout);

    app.route(baseUrl + '/:userId')
        .get(authenticate.setAuthenticatedUser, users.getOne);

    app.route(baseUrl + '/:userId/verify/:secretCode')
        .post(users.verifyEmail);

    app.route(baseUrl + '/:email/resend')
        .post(users.resendCode);

    app.route(baseUrl)
        .get(authenticate.adminRequired, users.get);

};
