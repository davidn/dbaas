angular.module('geniedb').factory('apiModel', function (dbaasConfig, $http, $resource) {
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
        {index: 12, code: 'starting', label: 'Starting launch', isAction: true},
        {index: 1, code: 'provisioning', label: 'Provisioning Instances', isAction: true},
        {index: 2, code: 'installing_cf', label: 'Installing GenieDB CloudFabric', isAction: true},
        {index: 13, code: 'configuring_monitoring', label: 'Configuring performance monitor', isAction: true},
        {index: 14, code: 'configuring_dns', label: 'Configuring DNS', isAction: true},
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
            node.isRunning = status.index === 3;
            node.isPaused = status.index === 4;
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

            cluster.canLaunch = cluster.status_code === 0;
            cluster.hasRunning = cluster.nodes.hasRunning;
            cluster.isRunning = cluster.status_code === 6;
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

});
