/**
 * Enhanced Select2 Dropmenus
 *
 * @AJAX Mode - When in this mode, your value will be an object (or array of objects) of the data used by Select2
 *     This change is so that you do not have to do an additional query yourself on top of Select2's own query
 * @params [options] {object} The configuration options passed to $.fn.select2(). Refer to the documentation
 */
angular.module('ui.select2collapsed', []).value('uiSelect2CollapsedConfig', {}).directive('uiSelect2Collapsed', ['uiSelect2CollapsedConfig', '$timeout', function (uiSelect2CollapsedConfig, $timeout) {
    var options = {};
    if (uiSelect2CollapsedConfig) {
        angular.extend(options, uiSelect2CollapsedConfig);
    }
    return {
        require: 'ngModel',
        priority: 1,
        compile: function (tElm, tAttrs) {
            var watch,
                repeatOption = tElm.find('optgroup[ng-repeat], optgroup[data-ng-repeat], option[ng-repeat], option[data-ng-repeat]'),
                repeatAttr,
                isSelect = tElm.is('select'),
                isMultiple = angular.isDefined(tAttrs.multiple);

            // Enable watching of the options dataset if in use
            if (tElm.is('select')) {
                repeatOption = tElm.find('option[ng-repeat], option[data-ng-repeat]');

                if (repeatOption.length) {
                    repeatAttr = repeatOption.attr('ng-repeat') || repeatOption.attr('data-ng-repeat');
                    watch = jQuery.trim(repeatAttr.split('|')[0]).split(' ').pop();
                }
            }

            return function (scope, elm, attrs, controller) {
                // instance-specific options
                var opts = angular.extend({}, options, scope.$eval(attrs.uiSelect2));

                /*
                 Convert from Select2 view-model to Angular view-model.
                 */
                var convertToAngularModel = function (select2_data) {
                    var model;
                    if (opts.simple_tags) {
                        model = [];
                        angular.forEach(select2_data, function (value, index) {
                            model.push(value.id);
                        });
                    } else {
                        model = select2_data;
                    }
                    return model;
                };

                /*
                 Convert from Angular view-model to Select2 view-model.
                 */
                var convertToSelect2Model = function (angular_data) {
                    var model = [];
                    if (!angular_data) {
                        return model;
                    }

                    if (opts.simple_tags) {
                        model = [];
                        angular.forEach(
                            angular_data,
                            function (value, index) {
                                model.push({'id': value, 'text': value});
                            });
                    } else {
                        model = angular_data;
                    }
                    return model;
                };

                if (isSelect) {
                    // Use <select multiple> instead
                    delete opts.multiple;
                    delete opts.initSelection;
                } else if (isMultiple) {
                    opts.multiple = true;
                }

                if (controller) {
                    controller.$render = function () {
                        if (isSelect) {
                            elm.select2('val', controller.$viewValue);
                        } else {
                            if (opts.multiple) {
                                var viewValue = controller.$viewValue;
                                if (angular.isString(viewValue)) {
                                    viewValue = viewValue.split(',');
                                }
                                elm.select2(
                                    'data', convertToSelect2Model(viewValue));
                            } else {
                                if (angular.isObject(controller.$viewValue)) {
                                    elm.select2('data', controller.$viewValue);
                                } else if (!controller.$viewValue) {
                                    elm.select2('data', null);
                                } else {
                                    elm.select2('val', controller.$viewValue);
                                }
                            }
                        }
                    };

                    // Watch the model for programmatic changes
//                    scope.$watch(tAttrs.ngModel, function (current, old) {
//                        if (current && current !== old) {
//                            controller.$render();
//                        } else {
//                            console.log('no current or values are equal');
//                        }
//                    }, true);

                    // Watch the options dataset for changes
                    if (watch) {
                        scope.$watch(watch, function (newVal, oldVal, scope) {
                            if (angular.equals(newVal, oldVal)) {
                                return;
                            }
                            // Delayed so that the options have time to be rendered
                            $timeout(function () {
                                elm.select2('val', controller.$viewValue);
                                // Refresh angular to remove the superfluous option
                                elm.trigger('change');
                                if (newVal && !oldVal && controller.$setPristine) {
                                    controller.$setPristine(true);
                                }
                            });
                        });
                    }

                    // Update valid and dirty statuses
                    controller.$parsers.push(function (value) {
                        var div = elm.prev();
                        div
                            .toggleClass('ng-invalid', !controller.$valid)
                            .toggleClass('ng-valid', controller.$valid)
                            .toggleClass('ng-invalid-required', !controller.$valid)
                            .toggleClass('ng-valid-required', controller.$valid)
                            .toggleClass('ng-dirty', controller.$dirty)
                            .toggleClass('ng-pristine', controller.$pristine);
                        return value;
                    });

                    if (!isSelect) {
                        // Set the view and model value and update the angular template manually for the ajax/multiple select2.
                        elm.bind("change", function (e) {
                            e.stopImmediatePropagation();

                            if (scope.$$phase || scope.$root.$$phase) {
                                return;
                            }
                            scope.$apply(function () {
                                controller.$setViewValue(
                                    convertToAngularModel(elm.select2('data')));
                            });
                        });

                        if (opts.initSelection) {
                            var initSelection = opts.initSelection;
                            opts.initSelection = function (element, callback) {
                                initSelection(element, function (value) {
                                    var isPristine = controller.$pristine;
                                    controller.$setViewValue(convertToAngularModel(value));
                                    callback(value);
                                    if (isPristine) {
                                        controller.$setPristine();
                                    }
                                    elm.prev().toggleClass('ng-pristine', controller.$pristine);
                                });
                            };
                        }
                    }
                }

                elm.bind("$destroy", function () {
                    elm.select2("destroy");
                });

                attrs.$observe('disabled', function (value) {
                    elm.select2('enable', !value);
                });

                attrs.$observe('readonly', function (value) {
                    elm.select2('readonly', !!value);
                });

                if (attrs.ngMultiple) {
                    scope.$watch(attrs.ngMultiple, function (newVal) {
                        attrs.$set('multiple', !!newVal);
                        elm.select2(opts);
                    });
                }

                // Initialize the plugin late so that the injected DOM does not disrupt the template compiler
                $timeout(function () {
                    elm.select2(opts);
                    //Modified code for making it collapsible (?)
                    elm.on('select2-open', function () {
                        $('div.select2-drop.select2-drop-active').children('ul.select2-results').children('li').children('div.select2-result-label').each(function () {
                            if ($(this).text().length > 0 && $(this).siblings('ul.select2-result-sub').children().length > 0) {
                                var collapsed = true;
                                $(this).prepend('<div class="label-arrow label-arrow-right"></div>');

                                $(this).siblings('ul.select2-result-sub').hide();
                                $(this).on('click', function () {
                                    if (!collapsed) {
                                        $(this).children('.label-arrow').removeClass('label-arrow-down').addClass('label-arrow-right');
                                        collapsed = true;
                                    } else {
                                        collapsed = false;
                                        $(this).children('.label-arrow').removeClass('label-arrow-right').addClass('label-arrow-down');
                                    }
                                    $(this).siblings('ul.select2-result-sub').toggle();
                                });
                            }
                        });
                    });

                    // Set initial value - I'm not sure about this but it seems to need to be there
                    elm.val(controller.$viewValue);
                    // important!
                    controller.$render();

                    // Not sure if I should just check for !isSelect OR if I should check for 'tags' key
                    if (!opts.initSelection && !isSelect) {
                        controller.$setViewValue(
                            convertToAngularModel(elm.select2('data'))
                        );
                    }
                });
            };
        }
    };
}]);
