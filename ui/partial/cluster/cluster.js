angular.module('geniedb').controller('ClusterCtrl', function ($scope, $location, $document, apiModel, growl, dbaasConfig) {
    $scope.providers = apiModel.getProviders();

    $scope.cluster = angular.copy(dbaasConfig.quickStart);
    $scope.showValidationMessages = false;

    $scope.save = function () {
        $scope.showValidationMessages = true;
        if (!apiModel.isUniqueClusterLabel($scope.cluster.label)) {
            growl.warning({body: "Cluster Name must be unique"});
            return;
        }
        $scope.isLoading = true;
        apiModel.Cluster.save($scope.cluster, function () {
            growl.success({body: "Cluster " + $scope.cluster.label + " created"});
            $location.path("/list");
        }, handleError);
    };

    $scope.cancel = function () {
        $location.path("/list");
    };

    function handleError(err) {
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