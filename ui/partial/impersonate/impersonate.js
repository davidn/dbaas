angular.module('geniedb').controller('ImpersonateCtrl', function ($location, $routeParams, User, growl) {
    User.setToken($routeParams.token);
    User.identify(true).$then(function () {
        $location.path("/list");
    }, function (err) {
        console.log('Impersonation Failed', err);
    });
});