angular.module('geniedb').controller('LogoutCtrl', function (User) {
    User.logout();
});