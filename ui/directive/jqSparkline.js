angular.module('geniedb').directive('Jqsparkline', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attrs, ngModel) {

            var opts = {};
            opts.type = attrs.type || 'line';

            scope.$watch(attrs.ngModel, function () {
                render();
            });

            scope.$watch(attrs.opts, function () {
                render();
            });

            var render = function () {
                var model = ngModel.$viewValue;
                var opts = {type: 'line'};
                if (attrs.opts) {
                    angular.extend(opts, angular.fromJson(attrs.opts));
                }
                if (model) {
                    if (attrs.composite) {
                        var optIndex = 0;
                        var composite = false;
                        for (var series in model) {
                            elem.sparkline(model[series], angular.extend({type: 'line', composite: composite}, opts[optIndex++]));
                            composite = true;
                        }
                    } else {
                        var data = angular.isArray(model) ? model : model.split(',');
                        elem.sparkline(data, opts);
                    }
                }
            };
        }
    };
});