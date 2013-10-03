
angular.module('GenieDBaaS.config', [])
    .constant('dbaasConfig', (function () {
        // TODO: Make conditional parameters for grunt.js to package the deployments
        var versionTag = "0.8";
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


        // TODO: Move quickStartFlavors to server side
        var quickStartFlavors={
            rs:"3",
            az:"m1.small",
            test:"test-small"
        };
        // TODO: Move launchTimes to server side
        var launchTimes={
            rs:5,
            az:3,
            test:1
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
            launchTimes: launchTimes,

            // TODO: Only used for $resource - purge if migrated off
            authUrlEscaped: escapedUrl + authPath,
            apiUrlEscaped: escapedUrl + apiPath,
            registerUrlEscaped: escapedUrl + registrationPath
        }
    })())