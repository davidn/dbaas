'use strict';
/*jslint node: true */

/* Controllers */

function MainCntl(User) {
    // Inject User to force initialization
}

function WelcomeCntl($scope, $location, User, growl) {
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
        // TODO - Forgot
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
            $location.path("/quickstart");
        }, function (err) {
            console.log(err);
            growl.error({body: 'Unable to activate account'});
        })
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

function ListCntl($scope, $location, apiModel, $http, growl, User, messageBox) {
//    TODO Disable UI while processing update on cluster
    if (!User.user.token) {
        $location.path("/");
        growl.error({body: "Session Expired"});
        return;
    }
    $scope.user = User.user;

    $scope.form = angular.copy($scope.user);
    $scope.providers = apiModel.getProviders();
    $scope.clusters = apiModel.getClusters(true);

    $scope.logout = function () {
        User.logout();
    };

    $scope.addCluster = function () {
        $location.path("/cluster");
    };

    $scope.launchCluster = function (cluster) {
        $http.post(cluster.url + '/launch_all/').success(function () {
            $scope.refresh();
        }).error(handleError);
    };

    $scope.addNode = function (cluster) {
        $location.path("/cluster/" + cluster.url.slice(-36) + "/node");
    }

    $scope.quickStart = function () {
        $location.path("/quickstart");
    };

    $scope.refresh = function () {
        $scope.isRefreshing = true;
        apiModel.getClusters(true).$then(function (data) {
            $scope.clusters = data.resource;
            $scope.isRefreshing = false;
        });
    };

    $scope.deleteCluster = function (cluster) {
        cluster.isDeleting = true;
        var title = 'Confirm';
        var msg = 'Are you sure you want to delete cluster ' + cluster.label + '?';
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
}

function ClusterCntl($scope, $location, apiModel, growl, dbaasConfig) {
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

function NodeCntl($scope, $routeParams, $location, apiModel, $http, growl, dbaasConfig) {
    $scope.providers = apiModel.getProviders();
    $scope.regions = apiModel.regions;

    $scope.save = function () {
        $scope.isLoading = true;

        var nodes = [
            {region: $scope.region.code,
                flavor: $scope.region.provider.quickStartFlavor,
                storage: 10}
        ];
        $http.post(dbaasConfig.apiUrl + "clusters/" + $routeParams.clusterid, nodes).success(function (data) {
            growl.success({body: "Node added in region " + $scope.region.name})
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
                    flavor: $scope.region1.provider.quickStartFlavor,
                    storage: 10},
                {region: $scope.region2,
                    label: "Quick Start Node 2",
                    flavor: $scope.region2.provider.quickStartFlavor,
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

