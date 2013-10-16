angular.module('geniedb').controller('TryCtrl', function ($scope, $location, User, growl) {

    $scope.form = angular.copy(User.user);
    $scope.isLoading = false;

    $scope.register = function () {
        $scope.isLoading = true;
        User.register($scope.form.email).$then(function () {
            $location.path("/thankyou");
        }, function (err) {
            $scope.isLoading = false;
            if (err && err.data) {
                growl.error({body: err.data});
            } else {
                growl.error({body: 'Registration Failed'});
            }
        });
    };
    $scope.cancel = function () {
        User.user.email = $scope.form.email;
        $location.path("/");
    };
});