angular.module('geniedb').controller('ActivateCtrl', function ($scope, $location, $route, $routeParams, User, growl) {

    $scope.statusText = "Looking up activation details...<i class='fa fa-refresh fa-spin'></i>";

    $scope.isReset = $route.current.$$route.action === 'reset';

    User.checkActivation($routeParams.activationHash).$then(function (response) {
        $scope.email = response.data.email;
    }, function (err) {
        $scope.statusText = "Activation code is not valid";
        growl.error({body: "Activation code is not valid"});
    });

    $scope.activate = function () {
        User.activate($routeParams.activationHash, $scope.password).$then(function (response) {
            growl.success({body: $scope.isReset ? "Password changed" : "Account activated!"});
            User.login($scope.email, $scope.password).$then(function () {
                if ($scope.isReset){
                    $location.path("/list");
                } else {
                    $location.path("/share/" + $scope.promo);
                }
            });
        }, function (err) {
            growl.error({body: "Unable to activate account"});
        });
    };
});