angular.module('Utility.directives', ['GenieDBaaS.config'])
    .directive('pwCheck', [function () {
        return {
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                var firstPassword = '#' + attrs.pwCheck;
                elem.add(firstPassword).on('keyup', function () {
                    scope.$apply(function () {
                        var v = elem.val() === $(firstPassword).val();
                        ctrl.$setValidity('pwmatch', v);
                    });
                });
            }
        }
    }])
    .directive('btnLoading', function () {
        return {
            link: function (scope, element, attrs) {
                scope.$watch(
                    function () {
                        return scope.$eval(attrs.btnLoading);
                    },
                    function (value) {
                        if (value) {
                            if (!attrs.hasOwnProperty('ngDisabled')) {
                                element.addClass('disabled').attr('disabled', 'disabled');
                            }

                            element.data('resetText', element.html());
                            element.html(element.data('loading-text'));
                        } else {
                            if (!attrs.hasOwnProperty('ngDisabled')) {
                                element.removeClass('disabled').removeAttr('disabled');
                            }

                            element.html(element.data('resetText'));
                        }
                    }
                );
            }
        };
    })
    .directive('appVersion', ['dbaasConfig', function (dbaasConfig) {
        return function (scope, elm, attrs) {
            elm.text(dbaasConfig.version);
        };
    }])
    .directive('jqSparkline', [function () {
        'use strict';
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
        }
    }])
    .directive('focusMe', function ($timeout, $parse) {
        return {
            link: function (scope, element, attrs) {
                $timeout(function () {
                    element[0].focus();
                });
            }
        };
    })
    // From https://gist.github.com/jbruni/6629714  pending PR https://github.com/angular-ui/bootstrap/pull/1046
    // TODO: Remove when PR rolled into Bootstrap-UI
    .run(["$templateCache", function ($templateCache) {
        $templateCache.put("template/popover/popover-template.html",
            "<div class=\"popover list-popover {{placement}}\" ng-class=\"{ in: isOpen(), fade: animation() }\">" +
                "  <div class=\"arrow\"><\/div>" +
                "  <div class=\"popover-inner\">" +
                "      <h3 class=\"popover-title\" ng-bind=\"title\" ng-show=\"title\"><\/h3>" +
                "      <div class=\"popover-content\"><\/div>" +
                "  <\/div>" +
                "<\/div>");
    }])
    .directive('popoverTemplatePopup', [ '$templateCache', '$compile', function ($templateCache, $compile) {
        return {
            restrict: 'EA',
            replace: true,
            scope: { title: '@', content: '@', placement: '@', animation: '&', isOpen: '&' },
            templateUrl: 'template/popover/popover-template.html',
            link: function (scope, iElement) {
                var content = angular.fromJson(scope.content),
                    template = $templateCache.get(content.templateUrl),
                    templateScope = scope,
                    scopeElements = document.getElementsByClassName('ng-scope');
                angular.forEach(scopeElements, function (element) {
                    var aScope = angular.element(element).scope();
                    if (aScope.$id == content.scopeId) {
                        templateScope = aScope;
                    }
                });
                iElement.find('div.popover-content').html($compile(template)(templateScope));
            }
        };
    }])
    .directive('popoverTemplate', [ '$tooltip', function ($tooltip) {
        var tooltip = $tooltip('popoverTemplate', 'popover', 'click');

        tooltip.compile = function () {
            return {
                'pre': function (scope, iElement, iAttrs) {
                    iAttrs.$set('popoverTemplate', { templateUrl: iAttrs.popoverTemplate, scopeId: scope.$id });
                },
                'post': tooltip.link
            };
        };

        return tooltip;
    }]);


angular.module('ui.directives', []);
angular.module('ui.directives').factory('keypressHelper', ['$parse', function keypress($parse) {
    var keysByCode = {
        8: 'backspace',
        9: 'tab',
        13: 'enter',
        27: 'esc',
        32: 'space',
        33: 'pageup',
        34: 'pagedown',
        35: 'end',
        36: 'home',
        37: 'left',
        38: 'up',
        39: 'right',
        40: 'down',
        45: 'insert',
        46: 'delete'
    };

    var capitaliseFirstLetter = function (string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    };

    return function (mode, scope, elm, attrs) {
        var params, combinations = [];
        params = scope.$eval(attrs['ui' + capitaliseFirstLetter(mode)]);

        // Prepare combinations for simple checking
        angular.forEach(params, function (v, k) {
            var combination, expression;
            expression = $parse(v);

            angular.forEach(k.split(' '), function (variation) {
                combination = {
                    expression: expression,
                    keys: {}
                };
                angular.forEach(variation.split('-'), function (value) {
                    combination.keys[value] = true;
                });
                combinations.push(combination);
            });
        });

        // Check only matching of pressed keys one of the conditions
        elm.bind(mode, function (event) {
            // No need to do that inside the cycle
            var altPressed = !!(event.metaKey || event.altKey);
            var ctrlPressed = !!event.ctrlKey;
            var shiftPressed = !!event.shiftKey;
            var keyCode = event.keyCode;

            // normalize keycodes
            if (mode === 'keypress' && !shiftPressed && keyCode >= 97 && keyCode <= 122) {
                keyCode = keyCode - 32;
            }

            // Iterate over prepared combinations
            angular.forEach(combinations, function (combination) {

                var mainKeyPressed = combination.keys[keysByCode[event.keyCode]] || combination.keys[event.keyCode.toString()];

                var altRequired = !!combination.keys.alt;
                var ctrlRequired = !!combination.keys.ctrl;
                var shiftRequired = !!combination.keys.shift;

                if (
                    mainKeyPressed &&
                        ( altRequired == altPressed ) &&
                        ( ctrlRequired == ctrlPressed ) &&
                        ( shiftRequired == shiftPressed )
                    ) {
                    // Run the function
                    scope.$apply(function () {
                        combination.expression(scope, { '$event': event });
                    });
                }
            });
        });
    };
}]);

/**
 * Bind one or more handlers to particular keys or their combination
 * @param hash {mixed} keyBindings Can be an object or string where keybinding expression of keys or keys combinations and AngularJS Exspressions are set. Object syntax: "{ keys1: expression1 [, keys2: expression2 [ , ... ]]}". String syntax: ""expression1 on keys1 [ and expression2 on keys2 [ and ... ]]"". Expression is an AngularJS Expression, and key(s) are dash-separated combinations of keys and modifiers (one or many, if any. Order does not matter). Supported modifiers are 'ctrl', 'shift', 'alt' and key can be used either via its keyCode (13 for Return) or name. Named keys are 'backspace', 'tab', 'enter', 'esc', 'space', 'pageup', 'pagedown', 'end', 'home', 'left', 'up', 'right', 'down', 'insert', 'delete'.
 * @example <input ui-keypress="{enter:'x = 1', 'ctrl-shift-space':'foo()', 'shift-13':'bar()'}" /> <input ui-keypress="foo = 2 on ctrl-13 and bar('hello') on shift-esc" />
 **/
angular.module('ui.directives').directive('uiKeydown', ['keypressHelper', function (keypressHelper) {
    return {
        link: function (scope, elm, attrs) {
            keypressHelper('keydown', scope, elm, attrs);
        }
    };
}]);

angular.module('ui.directives').directive('uiKeypress', ['keypressHelper', function (keypressHelper) {
    return {
        link: function (scope, elm, attrs) {
            keypressHelper('keypress', scope, elm, attrs);
        }
    };
}]);

angular.module('ui.directives').directive('uiKeyup', ['keypressHelper', function (keypressHelper) {
    return {
        link: function (scope, elm, attrs) {
            keypressHelper('keyup', scope, elm, attrs);
        }
    };
}]);

