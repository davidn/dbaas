angular.module('geniedb').directive('focusMe', function ($timeout) {
    return {
        link: function (scope, element, attrs) {
            $timeout(function () {
                element[0].focus();
            });
        }
    };
});