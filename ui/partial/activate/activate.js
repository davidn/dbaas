angular.module('geniedb').controller('ActivateCtrl', function ($scope, $location, $routeParams, User, growl) {

    $scope.statusText = "Looking up activation details...<i class='fa fa-refresh fa-spin'></i>";

    User.checkActivation($routeParams.activationHash).$then(function (response) {
        $scope.email = response.data.email;
    }, function (err) {
        $scope.statusText = "Activation code is not valid";
        console.log(err);
        growl.error({body: "Activation code is not valid"});
    });

    $scope.activate = function () {
        User.activate($routeParams.activationHash, $scope.password).$then(function (response) {
            growl.success({body: "Account activated!"});
            User.login($scope.email, $scope.password).$then(function () {
                $location.path("/share/" + $scope.promo);
            });
        }, function (err) {
            console.log(err);
            growl.error({body: "Unable to activate account"});
        });
    };
});