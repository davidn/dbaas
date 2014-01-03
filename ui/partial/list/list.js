angular.module('geniedb').controller('ListCtrl', function ($scope, $location, $timeout, apiModel, dbaasConfig, $http, growl, User, messageBox) {
    //    TODO Disable UI while processing update on cluster
    if (!User.user.token) {
        $location.path("/");
        growl.error({body: "Session Expired"});
        return;
    }

    User.identify();
    $scope.user = User.user;
    $scope.providers = apiModel.getProviders();

    $scope.addCluster = function () {
        $location.path("/cluster");
    };

    $scope.quickStart = function () {
        $location.path("/quickstart");
    };

    var refreshTimeout;

    $scope.refresh = function () {
        $timeout.cancel(refreshTimeout);
        $scope.isRefreshing = true;
        apiModel.getClusters(true).$then(function (data) {
            $scope.clusters = data.resource;
            $scope.isRefreshing = false;
            if ($scope.clusters && $scope.clusters.length > 0 && !$scope.clusters[0].hasRunning) {
                refreshTimeout = $timeout($scope.refresh, dbaasConfig.defaultRefresh);
            }
        });
    };

    $scope.refresh();

    $scope.launchCluster = function (cluster) {
        cluster.isLaunching = true;

        var title = 'Launching Cluster';
        var msg = apiModel.getLaunchMessage(_.pluck(cluster.nodes, 'provider'));
        var btns = [
            {result: 'ok', label: 'Ok', cssClass: 'btn-success'}
        ];
        messageBox.open(title, msg, btns);

        $http.post(cluster.url + '/launch_all/').success(function () {
            $scope.refresh();
        }).error(handleError);
    };

    $scope.addNode = function (cluster) {
        $location.path("/cluster/" + cluster.url.slice(-36) + "/node");
    };

    $scope.db = {name: ''};
    $scope.addDatabase = function (cluster) {
        if (_.contains(cluster.dbnames, $scope.db.name)) {
            growl.warning({body: "Database name must be unique"});
            return;
        }

        $scope.isLoading = true;
        $http.post(cluster.url + '/add_database', {dbname: $scope.db.name}).success(function () {
            growl.success({body: "Database " + $scope.db.name + " added to " + cluster.label + " cluster."});
            $scope.db = {name: ''};
            $scope.refresh();
            $scope.isLoading = false;
        }).error(handleError);
    };

    $scope.deleteCluster = function (cluster) {
        cluster.isDeleting = true;
        var title = 'Confirm';
        var msg = 'Are you sure you want to delete cluster <strong>' + cluster.label + '</strong>?';
        var btns = [
            {result: 'cancel', label: 'Cancel'},
            {result: 'ok', label: 'Delete', cssClass: 'btn-danger'}
        ];

        messageBox.open(title, msg, btns).result.then(function (result) {
            if (result === "ok") {
                $http['delete'](cluster.url).success(function () {
                    //TODO clean this up, this is just a temp solution
                    $timeout(function(){
                        $scope.refresh();
                    }, 50);
                    growl.success({body: "Cluster " + cluster.label + " shutting down"});
                }).error(function (err) {
                        cluster.isDeleting = false;
                        handleError(err);
                    });
            } else {
                cluster.isDeleting = false;
            }
        });
    };

    $scope.nodePause = function (node) {
        $http.post(node.url + '/pause').success(function () {
            $scope.refresh();
            growl.success({body: "Node " + node.label + " paused"});
        }).error(handleError);
    };

    $scope.nodeResume = function (node) {
        $http.post(node.url + '/resume').success(function () {
            $scope.refresh();
            growl.success({body: "Node " + node.label + " resumed"});
        }).error(handleError);
    };

    $scope.nodeUpgrade = function (node) {
        $location.path("/resize/" + node.id);
    };

    $scope.nodeDelete = function (node) {
        $http['delete'](node.url).success(function () {
            $scope.refresh();
        }).error(handleError);
    };

    function handleError(err) {
        $scope.isLoading = false;
        if (err && err.data && err.data.detail) {
            growl.error({body: err.data.detail});
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl.error({body: err.data.non_field_errors[0]});
        } else {
            growl.error({body: "Unable to Save"});
        }
    }

    $scope.$on('$destroy', function () {
        $timeout.cancel(refreshTimeout);
    });

});
