'use strict';
/*jslint node: true */

/* Controllers */

function MainCntl(User) {
    // Inject User to force initialization
}

function NavigationCtlr($scope, User) {
    $scope.user = User.user;

    $scope.logout = function () {
        User.logout();
    };
}

function WelcomeCntl($scope, $location, User, growl) {
    // TODO Refactor login flow
    if (User.user.token) {
        $location.path("/list");
        return;
    }

    $scope.form = angular.copy(User.user);
    $scope.showValidationMessages = false;
    $scope.isLoading = false;

    $scope.goRegister = function () {
        if ($scope.form && $scope.form.email) {
            User.user.email = $scope.form.email;
        }
        $location.path("try");
    };

    $scope.onForgot = function () {
        console.log("Add forgot view");
        // TODO - Forgot password
    };

    $scope.onLogin = function () {
        $scope.showValidationMessages = true;
        if ($scope.loginForm.$invalid) {
            return;
        }
        $scope.isLoading = true;
        User.login($scope.form.email, $scope.form.password).$then(function (data) {
            $location.path("/list");
        }, function (err) {
            $scope.isLoading = false;
            if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
                growl.error({body: err.data.non_field_errors[0]});
            } else {
                growl.error({body: 'Login Failed'});
            }
        });
    };
}

function ActivationCntl($scope, $location, $routeParams, User, growl) {
    $scope.statusText = "Looking up activation details...<i class='icon-refresh icon-spin'></i>";

    User.checkActivation($routeParams.activationHash).$then(function (response) {
        $scope.email = response.data.email;
    }, function (err) {
        $scope.statusText = "Activation code is not valid";
        console.log(err);
        growl.error({body: 'Activation code is not valid'});
    });

    $scope.activate = function () {
        User.activate($routeParams.activationHash, $scope.password).$then(function (response) {
            growl.success({body: 'Account activated!'});
            User.login($scope.email, $scope.password).$then(function () {
                $location.path("/quickstart");
            });
        }, function (err) {
            console.log(err);
            growl.error({body: 'Unable to activate account'});
        });
    }
}

function ThanksCntl() {
}

function RegisterCntl($scope, $location, User, growl) {
    $scope.form = angular.copy(User.user);
    $scope.isLoading = false;

    $scope.register = function () {
        $scope.isLoading = true;
        User.register($scope.form.email).$then(function () {
            $location.path("/thankyou");
        }, function (err) {
            $scope.isLoading = false;
            if (err && err.data) {
                growl.error({body: err.data});
            } else {
                growl.error({body: 'Registration Failed'});
            }
        });
    };
    $scope.cancel = function () {
        User.user.email = $scope.form.email;
        $location.path("/");
    };
}

function ListCntl($scope, $location, $timeout, apiModel, dbaasConfig, $http, growl, User, messageBox) {
//    TODO Disable UI while processing update on cluster
    // TODO: Add service to route onChange to confirm token existence
    if (!User.user.token) {
        $location.path("/");
        growl.error({body: "Session Expired"});
        return;
    }
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
        var providers = _.uniq(_.pluck(cluster.nodes, 'provider'));
        var launchTime = _.max(providers,function (provider) {
            return provider.launchTime;
        }).launchTime;
        console.log(providers);
        console.log(launchTime);
        var msg = 'We are now spinning up the cluster you requested.  You will receive an email when the cluster is available.  <br /><br />In general ' + _.pluck(providers, 'name').join(' and ') + ' take' + (providers.length > 1 ? '' : 's') + ' about ' + launchTime + ' minutes to provision and launch their nodes.';
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
    }

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
                $http.delete(cluster.url).success(function (data) {
                    $scope.refresh();
                    growl.success({body: "Cluster " + cluster.label + " deleted"});
                }).error(function (err) {
                        cluster.isDeleting = false;
                        handleError(err);
                    })
            }
            else {
                cluster.isDeleting = false;
            }
        });
    };

    $scope.deleteNode = function (node) {
        $http.delete(node.url).success(function (data) {
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
}

function ClusterCntl($scope, $location, $document, apiModel, growl, dbaasConfig) {
    $scope.providers = apiModel.getProviders();

    $scope.cluster = angular.copy(dbaasConfig.quickStart);

    $scope.save = function () {
        $scope.isLoading = true;
        apiModel.Cluster.save($scope.cluster, function () {
            growl.success({body: "Cluster " + $scope.cluster.label + " created"})
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
}

function NodeCntl($scope, $routeParams, $location, apiModel, $http, growl, dbaasConfig, User) {
    $scope.providers = apiModel.getProviders();

    // TODO: Set defaults
//        $scope.node = {region: apiModel.regions[0], flavor: apiModel.regions[0].provider.flavor[0], size:10};
    $scope.node = {size: 10};
    $scope.regions = apiModel.regions;
    $scope.user = User.user;

    $scope.updateFlavor = function () {
        $scope.node.flavor = $scope.node.region.provider.quickStartFlavor;
    }

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
            growl.success({body: "Node added in region " + node.region.name})
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
}


function QuickStartCntl($scope, $location, apiModel, $http, growl, dbaasConfig) {
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
                    $location.path('/list');
                }).error(handleError);
            }).error(handleError);
        }, handleError);
    };

    $scope.cancel = function () {
        $location.path('/list');
    }

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
}

