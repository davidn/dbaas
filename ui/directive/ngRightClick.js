angular.module('geniedb').directive('ngRightClick', function ($parse) {
    return function (scope, element, attrs) {
        var fn = $parse(attrs.ngRightClick);
        element.bind('contextmenu', function (event) {
            scope.$apply(function () {
                // TODO Make shift and ctrl configuration options for directive
                if (event.shiftKey && event.ctrlKey) {
                    event.preventDefault();
                    fn(scope, {$event: event});
                }
            });
        });
    };
});