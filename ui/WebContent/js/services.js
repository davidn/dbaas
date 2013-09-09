'use strict';
// TODO: Service to log errors server side

// TODO: Intercept HTTP 401 to login - add error message about session expired

angular.module('GenieDBaaS.services', ['GenieDBaaS.config', 'ngResource', 'ngStorage'])
    .factory("growl", function ($rootScope) {
        var queue = [], currentMessage = {};

        $rootScope.$on('$routeChangeSuccess', function () {
            if (queue.length > 0)
                currentMessage = queue.shift();
            else
                currentMessage = {};
        });

        return {
            set: function (message) {
                var msg = message;
                queue.push(msg);

            },
            get: function (message) {
                return currentMessage;
            },
            pop: function (message) {
                switch (message.type) {
                    case 'success':
                        toastr.success(message.body, message.title);
                        break;
                    case 'info':
                        toastr.info(message.body, message.title);
                        break;
                    case 'warning':
                        toastr.warning(message.body, message.title);
                        break;
                    case 'error':
                        toastr.error(message.body, message.title);
                        break;
                }
            },
            success: function (message) {
                toastr.success(message.body, message.title);
            },
            info: function (message) {
                toastr.info(message.body, message.title);
            },
            warning: function (message) {
                toastr.warning(message.body, message.title);
            },
            error: function (message) {
                toastr.error(message.body, message.title);
            }
        };
    })
    .factory("User", ['$resource', '$localStorage', '$http', 'dbaasConfig', '$location', function ($resource, $localStorage, $http, dbaasConfig, $location) {
        var user = $localStorage.$default({
            email: "",
            token: undefined
        });

        console.log(user);
        if (user.token) {
            $http.defaults.headers.common['Authorization'] = 'Token ' + user.token;
        }

        var Registration = $resource(dbaasConfig.authUrlEscaped + 'register/:activation_code', {activation_code: '@activation_code'});
        var User = $resource(dbaasConfig.authUrlEscaped + '/:id', {id: '@id'});

        return {
            user: user,
            register: function (email) {
                return Registration.save({email: email});
            },
            activate: function (activationCode) {

            },
            setPassword: function (id, password) {
                return Registration.save({id: id, password: password});
            },
            login: function (email, password) {
                user.email = email;
                return User.save({username: email, password: password}, function (data) {
                    user.token = data.token;
                    $http.defaults.headers.common['Authorization'] = 'Token ' + data.token;
                });
            },
            logout: function () {
                user.token = '';
                delete $http.defaults.headers.common['Authorization'];
                $location.path("/");
            }
        };
    }])
    .provider('apiModel', [function () {
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
                cluster.canLaunch = cluster.nodes.maxStatus === 0;
//            cluster.canLaunch = true;
                cluster.label = cluster.label || cluster.dbname;
            });
            return data;
        }


        this.$get = function ($resource, dbaasConfig) {

            Provider = $resource(dbaasConfig.apiUrlEscaped + 'providers');
            Cluster = $resource(dbaasConfig.apiUrlEscaped + 'clusters/:id/:command', {id: '@id', command: '@command'}, {
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
    }]);
