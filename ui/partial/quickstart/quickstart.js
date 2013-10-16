angular.module('geniedb').controller('QuickstartCtrl', function ($scope, $location, apiModel, $http, growl, dbaasConfig, messageBox) {
    $scope.providers = apiModel.getProviders();
    $scope.regions = apiModel.regions;

    $scope.launch = function () {
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
                    storage: 10},
                {region: $scope.region2.code,
                    label: "Quick Start Node 2",
                    flavor: $scope.region2.provider.quickStartFlavor.code,
                    storage: 10}
            ];
            $http.post(cluster.url, nodes).success(function () {
                growl.success({body: 'Quick start nodes created'});
                $http.post(cluster.url + '/launch_all/').success(function () {

                    var title = 'Launching Cluster';
                    var providers = _.uniq([$scope.region1.provider, $scope.region2.provider]);
                    var launchTime = _.max(providers,function (provider) {
                        return provider.launchTime;
                    }).launchTime;
                    var msg = 'We are now spinning up the cluster you requested.  You will receive an email when the cluster is available.  <br /><br />In general ' + _.pluck(providers, 'name').join(' and ') + ' take' + (providers.length > 1 ? '' : 's') + ' about ' + launchTime + ' minutes to provision and launch their nodes.';
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