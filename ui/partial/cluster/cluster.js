angular.module('geniedb').controller('ClusterCtrl', function ($scope, $location, apiModel, growl, dbaasConfig) {
    $scope.providers = apiModel.getProviders();
    $scope.cluster = angular.copy(dbaasConfig.quickStart);

    $scope.showValidationMessages = false;
    $scope.errorMessage = false;
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

    $scope.clusters = apiModel.getClusters(true).$then(function(data){
        $scope.clusters = data.resource;
        var unique = false;
        var quickIndex = 1;
        var newLabel = '';
        while(!unique) {
            newLabel = $scope.cluster.label + quickIndex;
            quickIndex++;
            unique = apiModel.isUniqueClusterLabel(newLabel);
        }
        $scope.cluster.label = newLabel;
    });

    function handleError(err) {
        $scope.isLoading = false;
        if (err && err.data && err.data.detail) {
            growl.error({body: err.data.detail});
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl.error({body: err.data.non_field_errors[0]});
        } else if(err && err.data && err.data && err.data.__all__) {
            $scope.errorMessage = err.data.__all__[0];
        } else {
            growl.error({body: 'Unable to save'});
        }
    }
});