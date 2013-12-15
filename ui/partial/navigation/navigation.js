angular.module('geniedb').controller('NavigationCtrl', function ($scope, User, $location) {
    $scope.user = User.user;

    $scope.logout = function () {
        User.logout();
    };

    $scope.upgrade = function () {
        $location.path("/upgrade");
    };

});