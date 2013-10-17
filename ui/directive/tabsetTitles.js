// This is a hack to allow tabsets to be used in repeaters
// Will generate errors on run, but the timeout cleans up the UI, so this works but floods the console with exceptions
// TODO: Replace when Angular UI Tabset bug is fixed
angular.module('geniedb').directive('tabsetTitles', function () {
    return {
        restrict: 'A',
        require: '^tabset',
        templateUrl: 'template/tabs/tabset-titles.html',
        replace: true,
        link: function (scope, elm, attrs, tabsetCtrl) {
            if (!scope.$eval(attrs.tabsetTitles)) {
                elm.remove();
            } else {
                setTimeout(function () {
                    //now that tabs location has been decided, transclude the tab titles in
                    tabsetCtrl.$transcludeFn(tabsetCtrl.$scope.$parent, function (node) {
                        elm.append(node);
                    });
                    scope.$apply();
                }, 0);
            }
        }
    };
});