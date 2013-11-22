angular.module('geniedb').controller('ForgotCtrl', function ($scope, User, $location, growl) {
    $scope.form = angular.copy(User.user);
    $scope.isLoading = false;
    $scope.submitted = false;

    $scope.reminder = function () {
        $scope.isLoading = true;

        User.reminder($scope.form.email).success(function () {
            $scope.submitted = true;
        }).error(function (err) {
            $scope.isLoading = false;
            if (err && err.data) {
                growl.error({body: err.data});
            } else {
                growl.error({body: "Sorry, we don't have that user email on file. Try again?"});
            }
        });
    };
    $scope.cancel = function () {
        User.user.email = $scope.form.email;
        $location.path("/");
    };

});