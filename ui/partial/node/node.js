angular.module('geniedb').controller('NodeCtrl', function ($scope, $routeParams, $location, apiModel, $http, growl, dbaasConfig, User) {
    $scope.providers = apiModel.getProviders();

    $scope.node = {size: 10};
    $scope.regions = apiModel.regions;
    $scope.user = User.user;

    $scope.updateFlavor = function () {
        $scope.node.flavor = $scope.node.region.provider.quickStartFlavor;
    };

    $scope.save = function () {
        $scope.isLoading = true;
        var node = $scope.node;

        var flavor = node.region.provider.quickStartFlavor;

        if (User.user.isPaid) {
            flavor = node.flavor;
            if (flavor.provider !== node.region.provider) {
                growl.error({body: "You must choose a valid provider for " + node.region.name});

                $scope.isLoading = false;
                return;
            }
        }

        var nodes = [
            {region: node.region.code,
                flavor: flavor.code,
                storage: node.size}
        ];
        // TODO Move to service call
        $http.post(dbaasConfig.apiUrl + "clusters/" + $routeParams.clusterid, nodes).success(function (data) {
            growl.success({body: "Node added in region " + node.region.name});
            $location.path('/list');
        }).error(handleError);
    };

    $scope.cancel = function () {
        $location.path("/list");
    };

    function handleError(err) {
        $scope.isLoading = false;
        if (err && err.detail) {
            growl.error({body: err.detail});
        } else if (err && err.non_field_errors && err.non_field_errors[0]) {
            growl.error({body: err.data.non_field_errors[0]});
        } else {
            growl.error({body: "Unable to save"});
        }
    }
});