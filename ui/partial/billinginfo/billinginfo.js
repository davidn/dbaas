angular.module('geniedb').controller('BillinginfoCtrl',function($scope, $location){

    $scope.cancel = function () {
        $location.path("/list");
    };
});