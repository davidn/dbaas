
angular.module('GenieDBaaS.config', [])
    .constant('dbaasConfig', (function () {
        // TODO: Make conditional parameters for grunt.js to package the deployments
        var versionTag = "0.2";
//        var serviceUrl = "http://localhost:8000";
        var serviceUrl= "https://dbaas-test.geniedb.com:4000";


        var defaultRefresh = 15000;

        var authPath = "/api-token-auth/";
        var apiPath = "/api/";
        var registrationPath = "/register/";
        var quickStartCluster = {
            label: "Quick Start Cluster",
            dbname: "quickstart",
            dbusername: "appuser",
            backup_schedule: "0 3,15 * * *",
            backup_count: "14",
            port: 3306
        };


        // TODO: Move this to server side
        var quickStartFlavors={
            rs:"3",
            az:"m1.small",
            test:"test-small"
        };

        // TODO: Only used for $resource - purge if migrated off
        var escapedUrl = serviceUrl.substr(0, 8) + serviceUrl.substr(8).replace(':', '\\:');

        return {
            version: versionTag,
            defaultRefresh: defaultRefresh,

            authUrl: serviceUrl + authPath,
            apiUrl: serviceUrl + apiPath,
            quickStart: quickStartCluster,
            quickStartFlavors: quickStartFlavors,

            // TODO: Only used for $resource - purge if migrated off
            authUrlEscaped: escapedUrl + authPath,
            apiUrlEscaped: escapedUrl + apiPath,
            registerUrlEscaped: escapedUrl + registrationPath
        }
    })())