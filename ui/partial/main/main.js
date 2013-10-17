angular.module('geniedb').controller('MainCtrl', function ($scope, User, dbaasConfig) {
    // Inject User to force initialization of Token
    $scope.showInfo = function () {
        console.log(dbaasConfig);
    };
});