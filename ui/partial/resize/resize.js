angular.module('geniedb').controller('ResizeCtrl', function ($scope, $routeParams, $location, apiModel, $http, growl, dbaasConfig, User) {

    $scope.providers = apiModel.getProviders();
    var node = apiModel.findNodeById($routeParams.clusterId, $routeParams.nodeId);
    if (node){
        $scope.flavor = node.$flavor;
        $scope.flavors = _.without(node.provider.flavors, node.$flavor);
        $scope.node = {flavor: node.$flavor};
    }

    $scope.user = User.user;

    $scope.save = function () {
        $scope.isLoading = true;
        var newNode = {url: node.url, flavor: $scope.node.flavor.code};
        // TODO Move to service call
        $http.put(dbaasConfig.apiUrl + "clusters/" + node.id, newNode).success(function (data) {
            growl.success({body: "Node resize in progress"});
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