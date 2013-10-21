angular.module('geniedb').directive('appEnvironment', function (dbaasConfig) {
    return function (scope, elm, attrs) {
        elm.text(dbaasConfig.environment);
    };
});