angular.module('geniedb').directive('appVersion', function (dbaasConfig) {
    return function (scope, elm, attrs) {
        elm.text(dbaasConfig.version);
    };
});