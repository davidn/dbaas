angular.module('geniedb').controller('ProfileCtrl', function ($scope, $http, $location, growl, User, dbaasConfig) {
    $scope.user = angular.copy(User.user);

    $scope.showValidationMessages = false;

    $scope.save = function () {
        $scope.showValidationMessages = true;
        // Validation Logic
        if ($scope.profileForm.$invalid){
            return;
        }

        $scope.isLoading = true;

        User.update({email: $scope.user.email, first_name: $scope.user.firstName, last_name: $scope.user.lastName, password: $scope.user.password}).success(function (data) {
            growl.success({body: "User data updated"});
            $location.path('/list');
        }).error(handleError);
    };

    $scope.cancel = function () {
        $location.path("/list");
    };

    function handleError(err) {
        console.log(err);
        $scope.isLoading = false;
        if (err && err.data && err.data.detail) {
            growl.error({body: err.data.detail});
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl.error({body: err.data.non_field_errors[0]});
        } else {
            growl.error({body: 'Unable to save'});
        }
    }
});