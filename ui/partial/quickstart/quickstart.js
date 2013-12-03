angular.module('geniedb').controller('QuickstartCtrl', function ($scope, $location, apiModel, $http, growl, dbaasConfig, messageBox) {
    $scope.providers = apiModel.getProviders();
    $scope.regions = apiModel.regions;
    $scope.showValidationMessages = false;

    $scope.launch = function () {
        $scope.showValidationMessages = true;
        if (!$scope.region1 || !$scope.region2) {
            growl.warning({body: 'Please select two regions for your Quick Start Cluster'});
            return;
        }

        $scope.isLoading = true;

        function generateKey(length) {
            return (Math.PI * Math.max(0.01, Math.random())).toString(36).substr(2, length);
        }

        dbaasConfig.quickStart.dbpassword = generateKey(10);

        apiModel.Cluster.save(dbaasConfig.quickStart, function (cluster) {
            growl.success({body: 'Cluster ' + cluster.label + ' created'});

            var nodes = [
                {region: $scope.region1.code,
                    label: "Quick Start Node 1",
                    flavor: $scope.region1.provider.quickStartFlavor.code,
                    storage: $scope.region1.provider.quickStartFlavor.variable_storage_default ? 10: null},
                {region: $scope.region2.code,
                    label: "Quick Start Node 2",
                    flavor: $scope.region2.provider.quickStartFlavor.code,
                    storage: $scope.region2.provider.quickStartFlavor.variable_storage_default ? 10: null}
            ];
            $http.post(cluster.url, nodes).success(function () {
                growl.success({body: 'Quick start nodes created'});
                $http.post(cluster.url + '/launch_all/').success(function () {
                    var title = 'Launching Cluster';
                    var msg = apiModel.getLaunchMessage([$scope.region1.provider, $scope.region2.provider]);
                    var btns = [
                        {result: 'ok', label: 'Ok', cssClass: 'btn-success'}
                    ];
                    messageBox.open(title, msg, btns);

                    $location.path('/list');
                }).error(handleError);
            }).error(handleError);
        }, handleError);
    };

    $scope.cancel = function () {
        $location.path('/list');
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