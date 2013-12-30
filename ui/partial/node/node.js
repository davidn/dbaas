angular.module('geniedb').controller('NodeCtrl', function ($scope, $routeParams, $location, apiModel, $http, growl, dbaasConfig, User) {
    $scope.providers = apiModel.getProviders();

    $scope.node = {size: 10, useVariableStorage: null};
    $scope.regions = apiModel.regions;
    $scope.user = User.user;
    $scope.isCollapsed = true;

    $scope.updateFlavor = function () {
        $scope.node.flavor = $scope.node.region.provider.quickStartFlavor;
        if ($scope.user.isPaid) {
            $scope.flavors = $scope.node.region.provider.flavors;
        }
        else {
            $scope.flavors = _.filter($scope.node.region.provider.flavors, 'free_allowed');
        }

        $scope.updateUseVariableStorage();
    };

    $scope.updateUseVariableStorage = function () {
        $scope.node.useVariableStorage = $scope.node.flavor.variable_storage_default;
        $scope.updateSize();
    };

    $scope.updateSize = function () {
        $scope.node.size = $scope.node.useVariableStorage ? 10 : $scope.node.flavor.fixed_storage;
//        alternative to change the default variable storage to the size of the fixed storage that would be used.
//        $scope.node.size = $scope.node.flavor.fixed_storage == null ? 10 : $scope.node.flavor.fixed_storage;
    };

    $scope.save = function () {
        if (!$scope.node.region) {
            growl.warning({body: 'Please select a node region to add to the cluster.'});
            return;
        }
        if (!$scope.node.flavor) {
            growl.warning({body: 'Please select a node type to add to the cluster.'});
            return;
        }
        $scope.isLoading = true;
        var node = $scope.node;

        var flavor = node.flavor;
        if (flavor.provider !== node.region.provider) {
            growl.error({body: "You must choose a valid provider for " + node.region.name});

            $scope.isLoading = false;
            return;
        }


        var nodes = [
            {region: node.region.code,
                flavor: flavor.code,
                storage: node.useVariableStorage ? node.size : null}
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

    $scope.toggle = function () {
        $scope.isCollapsed = !$scope.isCollapsed;
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