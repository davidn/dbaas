"use strict";
/*jslint node: true */

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

function ActivationCntl($scope, $routeParams) {
    $scope.hash = $routeParams.activationHash;
    //TODO: Get User Info
}

function ThanksCntl() {
}

function RegisterCntl($scope, $location, User, growl) {
    $scope.form = angular.copy(User.user);
    $scope.isLoading = false;

    $scope.register = function () {
        $scope.isLoading = true;
        User.register($scope.email).success(function () {
            $location.path("/thankyou");
        }).error(function (err) {
                $scope.isLoading = false;
                if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
                    growl.error({body: err.data.non_field_errors[0]});
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

function ListCntl($scope, $location, apiModel, $http, growl, User) {
    if (!User.user.token) {
        $location.path("/")
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

    $scope.addNode = function (cluster) {
        $location.path("/cluster/" + cluster.url.slice(-36) + "/node");
    }

    $scope.quickStart = function () {
        $location.path("/quickstart");
    };

    $scope.refresh = function () {
        $scope.clusters = apiModel.getClusters(true);
    };

    $scope.deleteCluster = function (cluster) {
        cluster.isDeleting = true;
        $http.delete(cluster.url).success(function (data) {
            $scope.refresh();
        }).error(function (err) {
                cluster.isDeleting = false;
                handleError(err);
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

function ClusterCntl($scope, $location, apiModel, growl) {
    $scope.providers = apiModel.getProviders();
    $scope.clusters = apiModel.getClusters();
    // Get User Info

    $scope.save = function () {
        $scope.isLoading = true;

        apiModel.getCluster().save(
            {label: "Quick Start Cluster",
                dbname: "quickstart",
                dbusername: "appuser",
                backup_schedule: "0 3,15 * * *",
                backup_count: "14",
                dbpassword: generateKey(10),
                port: 3306}, function () {
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

function NodeCntl($scope, $routeParams, $location, apiModel, $http) {
    $scope.providers = apiModel.getProviders();
    $scope.clusters = apiModel.getClusters();
    // Get User Info

    $scope.save = function () {
        $scope.isLoading = true;

        var nodes = [
            {region: $scope.quickStartNode1,
                flavor: getFlavorFromRegion($scope.quickStartNode1),
                storage: 10}
        ];
        $http.post(apiEndpointx + "clusters/" + $routeParams.clusterid, nodes).success(function (data) {
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

function getFlavorFromRegion(region) {
    return region.slice(0, 4) === "test" ? "test-small" : region.length === 3 ? "2" : "m1.small";
}

function QuickStartCntl($scope, $location, apiModel, $http, growl) {
    $scope.providers = apiModel.getProviders();

    $scope.launch = function () {
        $scope.isLoading = true;

        function generateKey(length) {
            return (Math.PI * Math.max(0.01, Math.random())).toString(36).substr(2, length);
        }

        apiModel.getCluster().save(
            {label: "Quick Start Cluster",
                dbname: "quickstart",
                dbusername: "appuser",
                backup_schedule: "0 3,15 * * *",
                backup_count: "14",
                dbpassword: generateKey(10),
                port: 3306}, function (cluster) {
                growl.success({body: 'Cluster ' + cluster.label + ' created'});
                var nodes = [
                    {region: $scope.quickStartNode1,
                        flavor: getFlavorFromRegion($scope.quickStartNode1),
                        storage: 10},
                    {region: $scope.quickStartNode2,
                        flavor: getFlavorFromRegion($scope.quickStartNode2),
                        storage: 10}
                ];
                $http.post(cluster.url, nodes).success(function (data) {
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

