'use strict';
// TODO: Service to log errors server side
// TODO: Change authenticator to provide user record along with token

angular.module('GenieDBaaS.services', ['GenieDBaaS.config', 'ngResource', 'ngStorage', 'ng'])
    .factory("growl", function ($rootScope) {

        // TODO: Clear messages on route success?
        $rootScope.$on('$routeChangeSuccess', function () {
        });
        return {
            success: function (message) {
                toastr.success(message.body, message.title, message);
            },
            info: function (message) {
                toastr.info(message.body, message.title, message);
            },
            warning: function (message) {
                toastr.warning(message.body, message.title, message);
            },
            error: function (message) {
                toastr.error(message.body, message.title, message);
            }
        };
    })
    .factory("User", ['$resource', '$localStorage', '$http', 'dbaasConfig', '$location', function ($resource, $localStorage, $http, dbaasConfig, $location) {
        var Registration = $resource(dbaasConfig.registerUrlEscaped + ':activation_code', {activation_code: '@activation_code'}, {
            activate: {method: 'PUT'}
        });
        var Token = $resource(dbaasConfig.authUrlEscaped + '/:id', {id: '@id'});
        var User = $resource(dbaasConfig.apiUrlEscaped + 'self', {}, {
            'identity': { method: 'GET', isArray: true }
        });
        var identityConfirmed = false;

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
                    plan: user.is_paid ? 'Paid' : 'Free'
                }
            }]);
            window.userEmail = user.email;
        }

        function setUser(aUser) {
            user.isPaid = aUser.is_paid;
            user.email = aUser.email;
            user.firstName = aUser.first_name;
            user.lastName = aUser.last_name;
            identityConfirmed = true;
            updateUserStorage();
            updateUserVoice();
        }

        function checkIdentity() {
            User.identity({}, function (data) {
                setUser(data);
            });
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
            reminder: function (email) {
                return Registration.activate({activation_code: activationCode}, {password: password});
            },
            login: function (email, password) {
                user.email = email;
                clearToken();
                return Token.save({username: email, password: password}, function (data) {
                    setToken(data.token);
                    checkIdentity();
                });
            },
            identify: function () {
                if (!identityConfirmed) {
                    checkIdentity();
                }
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
            {index: 0, code: 'initial', label: 'not yet started', isAction: false},
            {index: 1, code: 'provisioning', label: 'Provisioning Instances', isAction: true},
            {index: 2, code: 'installing_cf', label: 'Installing GenieDB CloudFabric', isAction: true},
            {index: 3, code: 'running', label: 'running', isAction: false},
            {index: 4, code: 'paused', label: 'paused', isAction: false},
            {index: 5, code: 'pausing', label: 'pausing', isAction: true},
            {index: 6, code: 'resuming', label: 'resuming', isAction: true},
            {index: 7, code: 'shutting_down', label: 'shutting down', isAction: true},
            {index: 8, code: 'over', label: 'over', isAction: false},
            {index: 9, code: 'error', label: 'An error occurred', isAction: false}
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
                node.isPaused = status.index == 4;
                node.isAction = status.isAction;

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

        function formatDataUrl(data) {
//            return 'data:text/plain;utf-8,'+ encodeURI(data);
            return (window.URL || window.webkitURL).createObjectURL(new Blob([ data ], { type: 'text/plain' }));
        }

        function hydrateClusterData(data) {
            data.forEach(function (cluster, i) {
                hydrateNodeData(i, cluster.nodes);
                if (cluster.ca_cert !== '') {
                    cluster.hasKeys = true;
                    cluster.ca_cert_url = formatDataUrl(cluster.ca_cert);
                    cluster.client_cert_url = formatDataUrl(cluster.client_cert);
                    cluster.client_key_url = formatDataUrl(cluster.client_key);
                } else {
                    cluster.hasKeys = false;
                }
                cluster.dbnames = _.uniq(cluster.dbname.split(','));
                cluster.dbnamesLabel = cluster.dbnames.length > 1 ? 'Databases' : 'Database';

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
                },
                addDatabase: {
                    method: "POST",
                    params: { command: 'add_database'}
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

    }])
    .factory("userVoice", function (dbaasConfig, User, growl) {
        return {
            contact: function (subject, message) {
                $.jsonp({
                    url: 'https://' + dbaasConfig.userVoiceSubdomain + '.uservoice.com/api/v1/tickets/create_via_jsonp.json?callback=?',
                    data: {
                        client: dbaasConfig.userVoiceClientKey,
                        ticket: {
                            message: message,
                            subject: subject
                        },
                        email: User.user.email
                    },
                    success: function (data) {
                        growl.success({body: 'Your request has been submitted, we will follow-up within one business day.', timeOut: 10000});
                    },
                    error: function (d, msg) {
                        growl.error({body: 'Unable to submit request.  Please try again.'});
                    }
                });
            }
        }
    });

