'use strict';
// TODO: Service to log errors server side
// TODO: Change authenticator to provide user record along with token

angular.module('GenieDBaaS.services', ['GenieDBaaS.config', 'ngResource', 'ngStorage', 'ng'])
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
        var Registration = $resource(dbaasConfig.registerUrlEscaped + ':activation_code', {activation_code: '@activation_code'}, {
            activate: {method: 'PUT'}
        });
        var Token = $resource(dbaasConfig.authUrlEscaped + '/:id', {id: '@id'});
        var User = $resource(dbaasConfig.apiUrlEscaped + 'users', {}, {
            'identity': { method: 'GET', isArray: true }
        });

        var user = $localStorage.$default({user: {email: "", isPaid: false, token: undefined}}).user;

        if (user.token) {
            $http.defaults.headers.common['Authorization'] = 'Token ' + user.token;
            updateUserVoice();
        }

        function clearToken() {
            user.token = '';
            delete $http.defaults.headers.common['Authorization'];
            updateUserStorage();
        }

        function setToken(token) {
            user.token = token;
            updateUserStorage();
            $http.defaults.headers.common['Authorization'] = 'Token ' + token;
        }

        function updateUserStorage() {
            $localStorage.user = user;
        }

        function updateUserVoice() {
            UserVoice.push(['identify', {
                email: user.email,
                account: {
                    name: user.email,
                    plan: user.is_paid ? 'Paid' : 'Free',
                }
            }]);
        }

        function setUser(aUser) {
            user.isPaid = aUser.is_paid;
            updateUserStorage();
            updateUserVoice();
        }

        return {
            user: user,
            register: function (email) {
                clearToken();
                return Registration.save({email: email});
            },
            checkActivation: function (activationCode) {
                clearToken();
                return Registration.get({activation_code: activationCode});
            },
            activate: function (activationCode, password) {
                clearToken();
                return Registration.activate({activation_code: activationCode}, {password: password});
            },
            login: function (email, password) {
                user.email = email;
                clearToken();
                return Token.save({username: email, password: password}, function (data) {
                    setToken(data.token);
                    User.identity({}, function (data) {
                        setUser(_.findWhere(data, {email: email}));
                    });
                });
            },
            logout: function () {
                clearToken();
                $location.path("/");
            }
        };
    }])
    .factory('apiModel', ['dbaasConfig', '$http', '$resource', function (dbaasConfig, $http, $resource) {
        var Provider;
        var Cluster;
        var providers;
        var clusters;
        var regions = [];
        var flavors = [];

        function getProviderByFlavor(flavorCode) {
            var flavor = _.findWhere(flavors, {code: flavorCode});
            return flavor && flavor.provider;
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
            data.hasRunning = false;
            data.forEach(function (node, i) {
                node.label = node.label ? node.label : node.region ? node.region : 'Node' + i;
                node.$flavor = _.findWhere(flavors, {code: node.flavor});
                node.provider = node.$flavor && node.$flavor.provider;
                node.$region = _.findWhere(regions, {code: node.region});
                var status = getStatusByLabel(node.status);
                node.statusClass = 'node-status-' + status.code;
                data.maxStatus = Math.max(status.index, data.maxStatus);
                node.isRunning = status.index == 3;
                data.hasRunning = data.hasRunning || node.isRunning;
                if (node.isRunning) {
                    $http.get(node.url + '/stats/').success(function (data) {
                        node.cpu = data.cpu ? data.cpu : [0];
                        node.iops = {read: data.riops, write: data.wiops};
                    });
                }
            });
            return data;
        }

        function hydrateClusterData(data) {
            data.forEach(function (cluster, i) {
                hydrateNodeData(i, cluster.nodes);
                cluster.canLaunch = cluster.nodes.maxStatus === 0;
                cluster.hasRunning = cluster.nodes.hasRunning;
                cluster.label = cluster.label || cluster.dbname;
            });
            return data;
        }

        function hydrateProviderData(data) {
            angular.forEach(dbaasConfig.quickStartFlavors, function (defaultFlavor, providerCode) {
                var provider = _.findWhere(providers, {code: providerCode});
                if (provider) {
                    provider.quickStartFlavor = _.findWhere(provider.flavors, {code: defaultFlavor});
                }
            });
            angular.forEach(dbaasConfig.launchTimes, function (launchTime, providerCode) {
                var provider = _.findWhere(providers, {code: providerCode});
                if (provider) {
                    provider.launchTime = launchTime;
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

    }]);
