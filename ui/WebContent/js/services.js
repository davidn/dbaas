'use strict';
// TODO: Service to log errors server side
// TODO: Set a default flavor for provider
// TODO: Hydrate provider to nodes

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
                queue.push(message);
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
        var user = $localStorage.$default({user: {
            email: "",
            token: undefined}
        }).user;

        if (user.token) {
            $http.defaults.headers.common['Authorization'] = 'Token ' + user.token;
        }

        var Registration = $resource(dbaasConfig.authUrlEscaped + 'register/:activation_code', {activation_code: '@activation_code'});
        var User = $resource(dbaasConfig.authUrlEscaped + '/:id', {id: '@id'});

        function clearToken() {
            user.token = '';
            delete $http.defaults.headers.common['Authorization'];
        }

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
                clearToken();
                return User.save({username: email, password: password}, function (data) {
                    user.token = data.token;
                    $http.defaults.headers.common['Authorization'] = 'Token ' + data.token;
                });
            },
            logout: function () {
                clearToken();
                $location.path("/");
            }
        };
    }])
    .provider('apiModel', ['dbaasConfig', function (dbaasConfig) {
        var Provider;
        var Cluster;
        var providers;
        var clusters;
        var regions = [];
        var flavors = [];

        function getProviderByFlavor(flavor) {
            return _.findWhere(flavors, {code: flavor}).provider;
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
            return _.findWhere(statuses, {label: statusLabel});
        }

        function hydrateNodeData(clusterIndex, data) {
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

        function hydrateClusterData(data) {
            data.forEach(function (cluster, i) {
                hydrateNodeData(i, cluster.nodes);
                cluster.canLaunch = cluster.nodes.maxStatus === 0;
                cluster.label = cluster.label || cluster.dbname;
            });
            return data;
        }

        function hydrateProviderData(data) {
            angular.forEach(dbaasConfig.quickStartFlavors, function (defaultFlavor, providerCode) {
                var provider = _.findWhere(providers, {code: providerCode});
                if (provider) {
                    provider.quickStartFlavor = defaultFlavor;
                }
            });
            regions.length = 0;
            flavors.length = 0;
            providers.forEach(function (provider) {
                provider.regions.forEach(function (region) {
                    region.provider = provider;
                });
                provider.flavors.forEach(function (flavor) {
                    flavor.provider = provider;
                });
                regions.push.apply(regions, provider.regions);
                flavors.push.apply(flavors, provider.flavors);
            });

            if (clusters && clusters.length > 0) {
                hydrateClusterData(clusters);
            }

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
                    providers = providers || Provider.query({}, hydrateProviderData);
                    return providers;
                },
                getClusters: function (forceRefresh) {
                    if (forceRefresh) {
                        clusters = Cluster.query({}, hydrateClusterData);
                    }
                    else {
                        clusters = clusters || Cluster.query({}, hydrateClusterData);
                    }
                    return clusters;
                },
                Cluster: Cluster,
                flavors: flavors,
                regions: regions
            };
        };
    }]);
