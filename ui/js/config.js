angular.module('geniedb').constant('dbaasConfig', (function () {
    var versionTag = "2.2.1";
    var buildTag = "%BUILDDATE%";
    //BEGINSERVICEURL
//    var serviceUrl = "//localhost:8000";
    var serviceUrl = "https://dbaas-test.geniedb.com:4000";
    //ENDSERVICEURL

    var posDash = serviceUrl.indexOf('-');
    var environmentLabel = posDash > 0 ? serviceUrl.substring(posDash+1,serviceUrl.indexOf('.')).toUpperCase():'';

    var userVoiceSubdomain = "geniedb";
    var userVoiceClientKey = "GyAUbnphymL97STPKy379g";

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
    var quickStartFlavors = {
        rs: "3",
        az: "m1.small",
        test: "test-small",
        gce: "g1-small"
    };
    // TODO: Move launchTimes to server side
    var launchTimes = {
        rs: 5,
        az: 3,
        test: 1
    };

    // TODO: Only used for $resource - purge if migrated off
    var escapedUrl = serviceUrl.substr(0, 8) + serviceUrl.substr(8).replace(':', '\\:');

    return {
        version: versionTag,
        build: buildTag,
        environment: environmentLabel,
        defaultRefresh: defaultRefresh,

        authUrl: serviceUrl + authPath,
        apiUrl: serviceUrl + apiPath,
        registerUrl: serviceUrl + registrationPath,
        quickStart: quickStartCluster,
        quickStartFlavors: quickStartFlavors,
        launchTimes: launchTimes,
        userVoiceSubdomain: userVoiceSubdomain,
        userVoiceClientKey: userVoiceClientKey,


        // TODO: Only used for $resource - purge once migrated off
        authUrlEscaped: escapedUrl + authPath,
        apiUrlEscaped: escapedUrl + apiPath,
        registerUrlEscaped: escapedUrl + registrationPath
    };
})());
