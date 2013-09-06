"use strict";
/*jslint node: true */

// TODO: Make conditional parameters for grunt.js to package the deployments
//var authEndpoint = "http://localhost\\:8000/api-token-auth/";
//var registrationEndpoint = "http://localhost\\:8000/";
//var apiEndpoint = "http://localhost\\:8000/api/";
//var apiEndpointx = "http://localhost:8000/api/";
var authEndpoint = "http://localhost\\:8000/api-token-auth/";
var registrationEndpoint = "http://localhost\\:8000/";
var apiEndpoint = "http://localhost\\:8000/api/";
var apiEndpointx = "http://localhost:8000/api/";
var Registration;
var User;

// TODO: Service to log errors server side
// TODO: Move btnLoading to library
// TODO: Intercept HTTP 401 to login - add error message about session expired

var dbaasApp = angular.module('GenieDBaaS', ['passwordChecker','ngRoute', 'ngSanitize', 'ngResource', 'ngStorage', 'ui.select2', 'angulartics', 'angulartics.google.analytics']).config(function ($routeProvider) {
    $routeProvider.
        when("/", {templateUrl: 'part/welcome.html', controller: WelcomeCntl}).
        when("/list", {templateUrl: 'part/list.html', controller: ListCntl}).
        when("/try", {templateUrl: 'part/try.html', controller: RegisterCntl}).
        when("/thankyou", {templateUrl: 'part/thanks.html', controller: ThanksCntl}).
        when("/activate/:activationHash", {templateUrl: 'part/activate.html', controller: ActivationCntl}).
        when("/quickstart", {templateUrl: 'part/quickstart.html', controller: QuickStartCntl}).
        when("/cluster", {templateUrl: 'part/cluster.html', controller: ClusterCntl}).
        when("/cluster/:clusterid/node", {templateUrl: 'part/node.html', controller: NodeCntl}).
        when("/monitor", {templateUrl: 'part/monitor.html', controller: QuickStartCntl}).
        otherwise({redirectTo: '/'});
}).directive('btnLoading', function () {
        return {
            link: function (scope, element, attrs) {
                scope.$watch(
                    function () {
                        return scope.$eval(attrs.btnLoading);
                    },
                    function (value) {
                        if (value) {
                            if (!attrs.hasOwnProperty('ngDisabled')) {
                                element.addClass('disabled').attr('disabled', 'disabled');
                            }

                            element.data('resetText', element.html());
                            element.html(element.data('loading-text'));
                        } else {
                            if (!attrs.hasOwnProperty('ngDisabled')) {
                                element.removeClass('disabled').removeAttr('disabled');
                            }

                            element.html(element.data('resetText'));
                        }
                    }
                );
            }
        };
    });

angular.module('passwordChecker', [])
	.directive('pwCheck', [function () {
	return {
		require: 'ngModel',
		link: function (scope, elem, attrs, ctrl) {
			var firstPassword = '#' + attrs.pwCheck;
			elem.add(firstPassword).on('keyup', function () {
				scope.$apply(function () {
					var v = elem.val()===$(firstPassword).val();
					ctrl.$setValidity('pwmatch', v);
				});
			});
		}
	}
}]);

// TODO: Move to service JS
dbaasApp.provider('apiModel', function () {
    var Provider;
    var Cluster;
    var providers;
    var clusters;


    function getFlavorByCode(flavors, code) {
        return flavors.filter(function (obj) {
            return obj.code === code;
        })[ 0 ];
    }

    function getProviderByFlavor(flavor) {
        return providers.filter(function (obj) {
            return getFlavorByCode(obj.flavors, flavor);
        })[ 0 ];
    }

    var statuses = [
        {index: 0, code: 'initial', label: 'not yet started'},
        {index: 1, code: 'provisioning', label: 'Provisioning Instances'},
        {index: 2, code: 'installing_cf', label: 'Installing GenieDB CloudFabric'},
        {index: 3, code: 'running', label: 'running'},
        {index: 4, code: 'paused', label: 'paused'},
        {index: 5, code: 'shutting_down', label: 'shutting down'},
        {index: 6, code: 'over', label: 'over'},
        {index: 7, code: 'error', label: 'An error occurred'}
    ];

    function getStatusByLabel(statusLabel) {
        return statuses.filter(function (status) {
            return status.label === statusLabel;
        })[0];
    }

    function lookupNodeData(clusterIndex, data) {
        data.maxStatus = 0;
        data.forEach(function (node, i) {
            node.label = node.label ? node.label : node.region ? node.region : 'Node' + i;
            node.provider = getProviderByFlavor(node.flavor);
            var status = getStatusByLabel(node.status);
            node.statusClass = 'node-status-' + status.code;
            data.maxStatus = Math.max(status.index, data.maxStatus);
            node.id = "node-" + clusterIndex + "-" + node.nid;
//        api_call('GET', node.url + 'stats/', {}, function (data) {
//            node.cpu = data.cpu;
//            node.riops = data.riops;
//            node.wiops = data.wiops;
//            $('#'+node.id+"-cpu").sparkline(node.cpu, {width:"100px"});
//            $('#'+node.id+"-iops").sparkline(node.riops, {width:"100px", lineColor:"#0F0"});
//            $('#'+node.id+"-iops").sparkline(node.wiops, {width:"100px", lineColor:"#F00", composite:true});
//            $.sparkline_display_visible();
//            }, generic_error);
        });
        return data;
    }

    function lookupClusterData(data) {
        data.forEach(function (cluster, i, arr) {
            lookupNodeData(i, cluster.nodes);
//            cluster.canLaunch = cluster.nodes.maxStatus === 0;
            cluster.canLaunch = true;
            cluster.label = cluster.label || cluster.dbname;
        });
        return data;
    }


    this.$get = function ($resource, $http, $localStorage) {
        Provider = $resource(apiEndpoint + 'providers');
        Cluster = $resource(apiEndpoint + 'clusters/:id/:command', {id: '@id', command: '@command'}, {
                addNodes: {
                    method: "POST"
                },
                launch: {
                    method: "POST",
                    params: { command: 'launch_all'}
                }
            }
        );
        return {
            getProviders: function () {
                providers = providers || Provider.query();
                return providers;
            },
            getClusters: function (forceRefresh) {
                if (forceRefresh) {
                    clusters = Cluster.query({}, lookupClusterData);
                }
                else {
                    clusters = clusters || Cluster.query({}, lookupClusterData);
                }
                return clusters;
            },
            getCluster: function () {
                return Cluster;
            }
        };
    };
});


function MainCntl($scope, $resource, $localStorage, $http) {
    $scope.alerts = [];
    Registration = $resource(registrationEndpoint + 'register/:activation_code', {activation_code: '@activation_code'});
    User = $resource(authEndpoint + '/:id', {id: '@id'});

    $scope.$storage = $localStorage.$default({
        user: {email: ""}
    });
    if ($scope.$storage.user.token){
        $http.defaults.headers.common['Authorization'] = 'Token ' + $scope.$storage.user.token;
    }
}

function WelcomeCntl($scope, $location, $http) {
    // Clear token if it exists
    $scope.alerts = [];
    $scope.form = angular.copy($scope.$storage.user);
    $scope.showValidationMessages = false;
    $scope.goRegister = function () {
        $scope.$storage.user.email = $scope.form.email;
        $location.path("try");
    };

    $scope.onForgot = function () {
        console.log("Add forgot view");
        // TODO - Forgot
    };

    $scope.onLogin = function () {
        $scope.showValidationMessages = true;
        if (!$scope.loginForm.$valid) {
            return;
        }
        $scope.isLoading = true;
        angular.copy($scope.form, $scope.$storage.user);
        User.save({username: $scope.$storage.user.email, password: $scope.$storage.user.password}, function (data) {
            $scope.alerts = [];
            $scope.$storage.user.token = data.token;
            $http.defaults.headers.common['Authorization'] = 'Token ' + data.token;
            $location.path("/list");
            $scope.isLoading = false;
        }, function (err) {
            $scope.isLoading = false;
            if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
                updateLoginError(err.data.non_field_errors[0]);
            } else {
                updateLoginError('Login Failed');
            }

        });
        $scope.$storage.user.password = undefined;
    }

    function updateLoginError(errorMessage) {
        $scope.alerts.push({ type: 'error', msg: errorMessage });
    }
}

function AlertCtrl($scope) {
    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };
}


function ActivationCntl($scope, $routeParams) {
    $scope.hash = $routeParams.activationHash;
    // Get User Info
}

function ThanksCntl($scope, $routeParams) {
    // Get User Info
}

function RegisterCntl($scope, $routeParams, $location) {
    $scope.form = angular.copy($scope.$storage.user);
    $scope.alerts = [];
    // Get User Info

    $scope.register = function () {
        $scope.isLoading = true;
        angular.copy($scope.form, $scope.$storage.user);
        Registration.save({email: $scope.$storage.user.email}, function () {
            $location.path("/thankyou");
            $scope.isLoading = false;
        }, function (err) {
            $scope.isLoading = false;
            console.log(err);
            if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
                updateLoginError(err.data.non_field_errors[0]);
            } else {
                updateLoginError('Registration Failed');
            }
        });
    };
    $scope.cancel = function () {
        angular.copy($scope.form, $scope.user);
        $location.path("/");
    };
    function updateLoginError(errorMessage) {
        $scope.alerts.push({ type: 'error', msg: errorMessage });
    }

}

function ListCntl($scope, $location, apiModel, $http, $localStorage) {
    if (!$localStorage.user.token){
        $location.path("/")
        return;
    }

    $scope.form = angular.copy($scope.user);
    $scope.alerts = [];
    $scope.providers = apiModel.getProviders();
    $scope.clusters = apiModel.getClusters(true);
    // TODO: If login token is invalid, redirect home

    $scope.logout = function () {
        // TODO Move this to a service
        delete $http.defaults.headers.common['Authorization'];

        $localStorage.user.token = "";
        $location.path("/");
    };

    $scope.addCluster = function () {
        $location.path("/cluster");
    };

    $scope.addNode = function (cluster) {
        console.log(cluster);
        $location.path("/cluster/" + cluster.url.slice(-36) + "/node");
    }

    $scope.quickStart = function () {
        $location.path("/quickstart");
    };

    $scope.refresh = function () {
        $scope.clusters = apiModel.getClusters(true);
    };

    $scope.deleteCluster = function (cluster) {
        $http.delete(cluster.url).success(function (data) {
            $scope.refresh();
        }).error(handleError);
    };

    $scope.deleteNode = function (node) {
          $http.delete(node.url).success(function (data) {
              $scope.refresh();
          }).error(handleError);
      };
    function handleError(err) {
        $scope.isLoading = false;
        if (err && err.data && err.data.detail) {
            growl('danger', err.data.detail);
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl('danger', err.data.non_field_errors[0]);
        } else {
            growl('danger', 'Unable to save');
        }
    }

    function growl(message) {
        $scope.alerts.push({ type: 'error', msg: message });
    }

}

function ClusterCntl($scope, $location, apiModel, $localStorage) {
    $scope.alerts = [];
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
            growl('danger', err.data.detail);
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl('danger', err.data.non_field_errors[0]);
        } else {
            growl('danger', 'Unable to save');
        }
    }

    function growl(type, message) {
        $scope.alerts.push({ type: type, msg: message });
    }
}

function NodeCntl($scope, $routeParams, $location, apiModel, $http) {
    $scope.alerts = [];
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
        console.log(err);
        $scope.isLoading = false;
        if (err && err.detail) {
            growl('danger', err.detail);
        } else if (err && err.non_field_errors && err.non_field_errors[0]) {
            growl('danger', err.non_field_errors[0]);
        } else {
            growl('danger', 'Unable to save');
        }
    }

    function growl(type, message) {
        $scope.alerts.push({ type: type, msg: message });
    }
}

function getFlavorFromRegion(region) {
    return region.slice(0, 4) === "test" ? "test-small" : region.length === 3 ? "2" : "m1.small";
}

function QuickStartCntl($scope, $location, apiModel, $http) {
// TODO Move off $http
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
                growl('info', 'Cluster ' + cluster.label + ' created');
                var nodes = [
                    {region: $scope.quickStartNode1,
                        flavor: getFlavorFromRegion($scope.quickStartNode1),
                        storage: 10},
                    {region: $scope.quickStartNode2,
                        flavor: getFlavorFromRegion($scope.quickStartNode2),
                        storage: 10}
                ];
                $http.post(cluster.url, nodes).success(function (data) {
                    growl('info', 'Quick start nodes created');
                    $http.post(cluster.url + '/launch_all/').success(function () {
                        $location.path('/list');
                    }).error(handleError);
                }).error(handleError);

            }, handleError);
    };


    function handleError(err) {
        $scope.isLoading = false;
        if (err && err.data && err.data.detail) {
            growl('danger', err.data.detail);
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl('danger', err.data.non_field_errors[0]);
        } else {
            growl('danger', 'Unable to save');
        }


    }

    function growl(type, message) {
        $scope.alerts.push({ type: type, msg: message });
    }
}

