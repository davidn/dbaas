angular.module('geniedb').controller('PricingCtrl', function ($scope, apiModel, $location, $timeout) {

    $scope.providers = apiModel.getProviders();

    $scope.regions = apiModel.regions;

    var defaultsTimeout;
    function setDefaults() {
        $timeout.cancel(defaultsTimeout);
        if ($scope.regions.length > 0) {
            $scope.region = $scope.regions[1];
        } else {
            defaultsTimeout = $timeout(setDefaults, 200);
        }
    }

    setDefaults();

    $scope.cancel = function () {
        $location.path("/list");
    };

    $scope.upgrade = function () {
        $location.path("/billinginfo");
    };

});