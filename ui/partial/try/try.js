angular.module('geniedb').controller('TryCtrl', function ($scope, $location, $timeout, User) {

    $scope.form = angular.copy(User.user);
    $scope.isLoading = false;
    $scope.form.error = false;
    $scope.register = function () {
        $scope.isLoading = true;
        User.register($scope.form.email).$then(function () {
            $location.path("/thankyou");
        }, function (err) {
            $scope.isLoading = false;
            if (err && err.data) {
                $scope.form.error = err.data.replace(/"/g, '');
            } else {
                $scope.form.error = 'Registration Failed';
            }
            $timeout(function(){
                $scope.form.error = false;
            }, 5000);
        });
    };
    $scope.cancel = function () {
        User.user.email = $scope.form.email;
        $location.path("/");
    };
});