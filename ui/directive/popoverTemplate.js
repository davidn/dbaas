// From https://gist.github.com/jbruni/6629714  pending PR https://github.com/angular-ui/bootstrap/pull/1046
// TODO: Remove when PR rolled into Bootstrap-UI
// This uses tooltipX to allow the custom templates to be patched in
angular.module('geniedb').run(function ($templateCache) {
    $templateCache.put("template/popover/popover-template.html",
        "<div class=\"popover list-popover {{placement}}\" ng-class=\"{ in: isOpen(), fade: animation() }\">" +
            "  <div class=\"arrow\"><\/div>" +
            "  <div class=\"popover-inner\">" +
            "      <button class=\"close close-sm\" ng-click=\"Hide()\">X<\/button>" +
            "      <h3 class=\"popover-title\" ng-bind=\"title\" ng-show=\"title\"><\/h3>" +
            "      <div class=\"popover-content\"><\/div>" +
            "  <\/div>" +
            "<\/div>");
})
    .directive('popoverTemplatePopup', function ($templateCache, $compile) {
        return {
            restrict: 'EA',
            replace: true,
            scope: { title: '@', content: '@', placement: '@', animation: '&', isOpen: '&', hide: '&' },
            templateUrl: 'template/popover/popover-template.html',
            link: function (scope, iElement) {
                var content = angular.fromJson(scope.content),
                    template = $templateCache.get(content.templateUrl),
                    templateScope = scope,
                    scopeElements = document.getElementsByClassName('ng-scope');
                angular.forEach(scopeElements, function (element) {
                    var aScope = angular.element(element).scope();
                    if (aScope.$id === content.scopeId) {
                        templateScope = aScope;
                    }
                });
                iElement.find('div.popover-content').html($compile(template)(templateScope));
            },
            controller: function ($scope) {
                $scope.Hide = function () {
                    $scope.hide();
                };
            }
        };
    })
    .directive('popoverTemplate', function ($tooltipX) {
        var tooltip = $tooltipX('popoverTemplate', 'popover', 'click');

        tooltip.compile = function () {
            return {
                'pre': function (scope, iElement, iAttrs) {
                    iAttrs.$set('popoverTemplate', { templateUrl: iAttrs.popoverTemplate, scopeId: scope.$id });
                },
                'post': tooltip.link
            };
        };

        return tooltip;
    });
