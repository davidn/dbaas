// TODO: Make conditional parameters for grunt.js to package the deployments

angular.module('GenieDBaaS.config', [])
    .constant('dbaasConfig', (function () {
        var serviceUrl = "http://localhost:8000";
//        var serviceUrl= "https://dbaas-test.geniedb.com:4000";
        var authPath = "/api-token-auth/";
        var apiPath = "/api/";
        // TODO: Only used for $resource - purge if migrated off
        var escapedUrl = serviceUrl.substr(0,8) + serviceUrl.substr(8).replace(':', '\\:');

        return {
            version: '0.2',

            authUrl: serviceUrl + authPath,
            apiUrl: serviceUrl + apiPath,
            // TODO: Only used for $resource - purge if migrated off
            authUrlEscaped: escapedUrl + authPath,
            apiUrlEscaped: escapedUrl + apiPath
        }
    })())