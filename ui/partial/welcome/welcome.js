angular.module('geniedb').controller('WelcomeCtrl', function ($scope, $location, User, growl) {
    if (User.user.token) {
        $location.path("/list");
        return;
    }

    $scope.form = angular.copy(User.user);
    $scope.showValidationMessages = false;
    $scope.isLoading = false;

    $scope.goRegister = function () {
        if ($scope.form && $scope.form.email) {
            User.user.email = $scope.form.email;
        }
        $location.path("try");
    };

    $scope.onForgot = function () {
        $location.path("forgot");
    };

    $scope.onLogin = function () {
        $scope.showValidationMessages = true;
        if ($scope.loginForm.$invalid) {
            return;
        }
        $scope.isLoading = true;
        User.login($scope.form.email, $scope.form.password).$then(function (data) {
            $location.path("/list");
        }, function (err) {
            $scope.isLoading = false;
            if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
                $scope.form.errors = err.data.non_field_errors;
            } else {
                //Check what these errors look like and come up with a way to handle them
                growl.error({body: 'Login Failed'});
            }
        });
    };
});