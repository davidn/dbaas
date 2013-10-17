angular.module('geniedb').controller('NavigationCtrl', function ($scope, User, userVoice) {
    $scope.user = User.user;

    $scope.logout = function () {
        User.logout();
    };

    $scope.upgrade = function () {
        userVoice.contact('Upgrade Account', 'Interested in upgrading to paid account.');
    };

});