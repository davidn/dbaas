angular.module('geniedb').factory('apiModel', function (dbaasConfig, $http, $resource) {
    var Provider;
    var Cluster;
    var providers;
    var clusters;
    var regions = [];
    var flavors = [];

    var statuses = [
        {index: 0, code: 'initial', label: 'not yet started', isAction: false},
        {index: 12, code: 'starting', label: 'Starting launch', isAction: true},
        {index: 1, code: 'provisioning', label: 'Provisioning Instances', isAction: true},
        {index: 2, code: 'installing_cf', label: 'Installing GenieDB CloudFabric', isAction: true},
        {index: 13, code: 'configuring_monitoring', label: 'Configuring performance monitor', isAction: true},
        {index: 14, code: 'configuring_dns', label: 'Configuring DNS', isAction: true},
        {index: 15, code: 'configuring_node', label: 'Configuring node', isAction: true},
        {index: 3, code: 'running', label: 'running', isAction: false},
        {index: 4, code: 'paused', label: 'paused', isAction: false},
        {index: 5, code: 'pausing', label: 'pausing', isAction: true},
        {index: 6, code: 'resuming', label: 'resuming', isAction: true},
        {index: 7, code: 'shutting_down', label: 'shutting down', isAction: true},
        {index: 8, code: 'over', label: 'over', isAction: false},
        {index: 9, code: 'error', label: 'An error occurred', isAction: false}
        {index: 16, code: 'copying', label: 'Copying data', isAction: true}
    ];

    var allowedNodeStatesForAddNode = [0, 3, 4, 5, 7, 8];
    var allowedNodeStatesForUpgradeNode = [0, 3, 4];

    function serialComma(arr) {
        if (arr.length <= 2){
            return arr.join(' and ');
        }
        arr[arr.length-1] = 'and ' + arr[arr.length-1];
        return arr.join(', ');
    }

    function getLaunchMessage(providerList) {
        var providers = _.uniq(providerList);
        var launchTime = _.max(providers,function (provider) {
            return provider.launchTime;
        }).launchTime;
        return 'We are now spinning up the cluster you requested.  You will receive an email with <strong>connection instructions</strong> when the cluster is available.  <br /><br />In general ' +
            serialComma(_.pluck(providers, 'name')) + ' take' + (providers.length > 1 ? '' : 's') + ' about ' + launchTime + ' minutes to provision and launch their nodes.';
    }

    function isUniqueClusterLabel(clusterLabel) {
        return _.findWhere(clusters, {label: clusterLabel}) === undefined;
    }

    function getStatusByLabel(statusLabel) {
        return _.findWhere(statuses, {label: statusLabel});
    }

    function hydrateNodeData(data) {
        data.maxStatus = 0;
        data.hasRunning = false;
        data.canAddNode = true;
        data.forEach(function (node, i) {
            node.label = node.label ? node.label : node.region ? node.region : 'Node' + i;
            node.$flavor = _.findWhere(flavors, {code: node.flavor});
            node.provider = node.$flavor && node.$flavor.provider;
            node.$region = _.findWhere(regions, {code: node.region});
            var status = getStatusByLabel(node.status);
            node.statusClass = 'node-status-' + status.code;
            data.maxStatus = Math.max(status.index, data.maxStatus);

            var fragments = node.url.split('/');
            node.id = fragments.slice(-2).join('/');
            node.uid = fragments[fragments.length-1];

            node.isRunning = status.index === 3;
            node.isPaused = status.index === 4;
            node.isAction = status.isAction;
            node.canUpgrade = allowedNodeStatesForUpgradeNode.indexOf(status.index) >= 0;

            data.hasRunning = data.hasRunning || node.isRunning;
            data.canAddNode = data.canAddNode && (allowedNodeStatesForAddNode.indexOf(status.index) >= 0);
            if (node.isRunning) {
                $http.get(node.url + '/stats/').success(function (data) {
                    node.cpu = data.cpu ? data.cpu : [0];
                    node.iops = {read: data.riops, write: data.wiops};
                });

                if (!node.backups) {
                    node.backups = [];
                    $http.get(node.url + '/backups/').success(function (data) {
                        node.backups = data.reverse();
                        node.backups.forEach(function (backup) {
                            backup.size = numeral(backup.size).format('0.0b');
                            backup.time = moment(backup.time).calendar();
                        });
                    });
                }
            }
        });
        return data;
    }

    function formatDataUrl(data) {
        return (window.URL || window.webkitURL).createObjectURL(new Blob([ data ], { type: 'text/plain' }));
    }

    function hydrateClusterData(data) {
        data.forEach(function (cluster) {
            hydrateNodeData(cluster.nodes);
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

            cluster.canLaunch = cluster.status_code === 0 && cluster.nodes && cluster.nodes.length > 0;
            cluster.hasRunning = cluster.nodes.hasRunning;
            cluster.isRunning = cluster.status_code === 6;
            cluster.label = cluster.label || cluster.dbname;
            cluster.canAddNode = cluster.status_code === 0 || (cluster.status_code === 6 && cluster.nodes.canAddNode);
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
                // TODO: REMOVE HACK
                flavor.price = 0.04;
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
            } else {
                clusters = clusters || Cluster.query({}, hydrateClusterData);
            }
            return clusters;
        },
        findNodeById: function (clusterId, nodeId){
            var cluster = _.findWhere(clusters, {id: clusterId});
            return cluster && _.findWhere(cluster.nodes, {uid: nodeId});
        },
        getLaunchMessage: getLaunchMessage,
        isUniqueClusterLabel: isUniqueClusterLabel,
        Cluster: Cluster,
        flavors: flavors,
        regions: regions
    };

});
