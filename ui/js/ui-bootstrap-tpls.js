//TODO: Move to distributed version once the PR is published  https://github.com/angular-ui/bootstrap/pull/1171

angular.module("ui.bootstrap", ["ui.bootstrap.tpls", "ui.bootstrap.transition", "ui.bootstrap.collapse", "ui.bootstrap.accordion", "ui.bootstrap.alert", "ui.bootstrap.bindHtml", "ui.bootstrap.buttons", "ui.bootstrap.position", "ui.bootstrap.dropdownToggle", "ui.bootstrap.modal", "ui.bootstrap.pagination", "ui.bootstrap.tooltip", "ui.bootstrap.popover", "ui.bootstrap.progressbar", "ui.bootstrap.rating", "ui.bootstrap.tabs", "ui.bootstrap.timepicker", "ui.bootstrap.typeahead"]);
angular.module("ui.bootstrap.tpls", ["template/accordion/accordion-group.html", "template/accordion/accordion.html", "template/alert/alert.html", "template/modal/backdrop.html", "template/modal/window.html", "template/pagination/pager.html", "template/pagination/pagination.html", "template/tooltip/tooltip-html-unsafe-popup.html", "template/tooltip/tooltip-popup.html", "template/popover/popover.html", "template/progressbar/bar.html", "template/progressbar/progress.html", "template/rating/rating.html", "template/tabs/tab.html", "template/tabs/tabset-titles.html", "template/tabs/tabset.html", "template/timepicker/timepicker.html", "template/typeahead/typeahead-match.html", "template/typeahead/typeahead-popup.html"]);
angular.module('ui.bootstrap.transition', [])

/**
 * $transition service provides a consistent interface to trigger CSS 3 transitions and to be informed when they complete.
 * @param  {DOMElement} element  The DOMElement that will be animated.
 * @param  {string|object|function} trigger  The thing that will cause the transition to start:
 *   - As a string, it represents the css class to be added to the element.
 *   - As an object, it represents a hash of style attributes to be applied to the element.
 *   - As a function, it represents a function to be called that will cause the transition to occur.
 * @return {Promise}  A promise that is resolved when the transition finishes.
 */
    .factory('$transition', ['$q', '$timeout', '$rootScope', function ($q, $timeout, $rootScope) {

        var $transition = function (element, trigger, options) {
            options = options || {};
            var deferred = $q.defer();
            var endEventName = $transition[options.animation ? "animationEndEventName" : "transitionEndEventName"];

            var transitionEndHandler = function (event) {
                $rootScope.$apply(function () {
                    element.unbind(endEventName, transitionEndHandler);
                    deferred.resolve(element);
                });
            };

            if (endEventName) {
                element.bind(endEventName, transitionEndHandler);
            }

            // Wrap in a timeout to allow the browser time to update the DOM before the transition is to occur
            $timeout(function () {
                if (angular.isString(trigger)) {
                    element.addClass(trigger);
                } else if (angular.isFunction(trigger)) {
                    trigger(element);
                } else if (angular.isObject(trigger)) {
                    element.css(trigger);
                }
                //If browser does not support transitions, instantly resolve
                if (!endEventName) {
                    deferred.resolve(element);
                }
            });

            // Add our custom cancel function to the promise that is returned
            // We can call this if we are about to run a new transition, which we know will prevent this transition from ending,
            // i.e. it will therefore never raise a transitionEnd event for that transition
            deferred.promise.cancel = function () {
                if (endEventName) {
                    element.unbind(endEventName, transitionEndHandler);
                }
                deferred.reject('Transition cancelled');
            };

            return deferred.promise;
        };

        // Work out the name of the transitionEnd event
        var transElement = document.createElement('trans');
        var transitionEndEventNames = {
            'WebkitTransition': 'webkitTransitionEnd',
            'MozTransition': 'transitionend',
            'OTransition': 'oTransitionEnd',
            'transition': 'transitionend'
        };
        var animationEndEventNames = {
            'WebkitTransition': 'webkitAnimationEnd',
            'MozTransition': 'animationend',
            'OTransition': 'oAnimationEnd',
            'transition': 'animationend'
        };

        function findEndEventName(endEventNames) {
            for (var name in endEventNames) {
                if (transElement.style[name] !== undefined) {
                    return endEventNames[name];
                }
            }
        }

        $transition.transitionEndEventName = findEndEventName(transitionEndEventNames);
        $transition.animationEndEventName = findEndEventName(animationEndEventNames);
        return $transition;
    }]);

angular.module('ui.bootstrap.collapse', ['ui.bootstrap.transition'])

// The collapsible directive indicates a block of html that will expand and collapse
    .directive('collapse', ['$transition', function ($transition) {
        // CSS transitions don't work with height: auto, so we have to manually change the height to a
        // specific value and then once the animation completes, we can reset the height to auto.
        // Unfortunately if you do this while the CSS transitions are specified (i.e. in the CSS class
        // "collapse") then you trigger a change to height 0 in between.
        // The fix is to remove the "collapse" CSS class while changing the height back to auto - phew!
        var fixUpHeight = function (scope, element, height) {
            // We remove the collapse CSS class to prevent a transition when we change to height: auto
            element.removeClass('collapse');
            element.css({ height: height });
            // It appears that  reading offsetWidth makes the browser realise that we have changed the
            // height already :-/
            var x = element[0].offsetWidth;
            element.addClass('collapse');
        };

        return {
            link: function (scope, element, attrs) {

                var isCollapsed;
                var initialAnimSkip = true;

                scope.$watch(attrs.collapse, function (value) {
                    if (value) {
                        collapse();
                    } else {
                        expand();
                    }
                });


                var currentTransition;
                var doTransition = function (change) {
                    if (currentTransition) {
                        currentTransition.cancel();
                    }
                    currentTransition = $transition(element, change);
                    currentTransition.then(
                        function () {
                            currentTransition = undefined;
                        },
                        function () {
                            currentTransition = undefined;
                        }
                    );
                    return currentTransition;
                };

                var expand = function () {
                    if (initialAnimSkip) {
                        initialAnimSkip = false;
                        if (!isCollapsed) {
                            fixUpHeight(scope, element, 'auto');
                            element.addClass('in');
                        }
                    } else {
                        element.addClass('in');
                        doTransition({ height: element[0].scrollHeight + 'px' })
                            .then(function () {
                                // This check ensures that we don't accidentally update the height if the user has closed
                                // the group while the animation was still running
                                if (!isCollapsed) {
                                    fixUpHeight(scope, element, 'auto');
                                    element.addClass('in');
                                }
                            });
                    }
                    isCollapsed = false;
                };

                var collapse = function () {
                    isCollapsed = true;
                    element.removeClass('in');
                    if (initialAnimSkip) {
                        initialAnimSkip = false;
                        fixUpHeight(scope, element, 0);
                    } else {
                        fixUpHeight(scope, element, element[0].scrollHeight + 'px');
                        doTransition({'height': '0'});
                    }
                };
            }
        };
    }]);

angular.module('ui.bootstrap.accordion', ['ui.bootstrap.collapse'])

    .constant('accordionConfig', {
        closeOthers: true
    })

    .controller('AccordionController', ['$scope', '$attrs', 'accordionConfig', function ($scope, $attrs, accordionConfig) {

        // This array keeps track of the accordion groups
        this.groups = [];

        // Ensure that all the groups in this accordion are closed, unless close-others explicitly says not to
        this.closeOthers = function (openGroup) {
            var closeOthers = angular.isDefined($attrs.closeOthers) ? $scope.$eval($attrs.closeOthers) : accordionConfig.closeOthers;
            if (closeOthers) {
                angular.forEach(this.groups, function (group) {
                    if (group !== openGroup) {
                        group.isOpen = false;
                    }
                });
            }
        };

        // This is called from the accordion-group directive to add itself to the accordion
        this.addGroup = function (groupScope) {
            var that = this;
            this.groups.push(groupScope);

            groupScope.$on('$destroy', function (event) {
                that.removeGroup(groupScope);
            });
        };

        // This is called from the accordion-group directive when to remove itself
        this.removeGroup = function (group) {
            var index = this.groups.indexOf(group);
            if (index !== -1) {
                this.groups.splice(this.groups.indexOf(group), 1);
            }
        };

    }])

// The accordion directive simply sets up the directive controller
// and adds an accordion CSS class to itself element.
    .directive('accordion', function () {
        return {
            restrict: 'EA',
            controller: 'AccordionController',
            transclude: true,
            replace: false,
            templateUrl: 'template/accordion/accordion.html'
        };
    })

// The accordion-group directive indicates a block of html that will expand and collapse in an accordion
    .directive('accordionGroup', ['$parse', '$transition', '$timeout', function ($parse, $transition, $timeout) {
        return {
            require: '^accordion',         // We need this directive to be inside an accordion
            restrict: 'EA',
            transclude: true,              // It transcludes the contents of the directive into the template
            replace: true,                // The element containing the directive will be replaced with the template
            templateUrl: 'template/accordion/accordion-group.html',
            scope: { heading: '@' },        // Create an isolated scope and interpolate the heading attribute onto this scope
            controller: ['$scope', function ($scope) {
                this.setHeading = function (element) {
                    this.heading = element;
                };
            }],
            link: function (scope, element, attrs, accordionCtrl) {
                var getIsOpen, setIsOpen;

                accordionCtrl.addGroup(scope);

                scope.isOpen = false;

                if (attrs.isOpen) {
                    getIsOpen = $parse(attrs.isOpen);
                    setIsOpen = getIsOpen.assign;

                    scope.$watch(
                        function watchIsOpen() {
                            return getIsOpen(scope.$parent);
                        },
                        function updateOpen(value) {
                            scope.isOpen = value;
                        }
                    );

                    scope.isOpen = getIsOpen ? getIsOpen(scope.$parent) : false;
                }

                scope.$watch('isOpen', function (value) {
                    if (value) {
                        accordionCtrl.closeOthers(scope);
                    }
                    if (setIsOpen) {
                        setIsOpen(scope.$parent, value);
                    }
                });
            }
        };
    }])

// Use accordion-heading below an accordion-group to provide a heading containing HTML
// <accordion-group>
//   <accordion-heading>Heading containing HTML - <img src="..."></accordion-heading>
// </accordion-group>
    .directive('accordionHeading', function () {
        return {
            restrict: 'EA',
            transclude: true,   // Grab the contents to be used as the heading
            template: '',       // In effect remove this element!
            replace: true,
            require: '^accordionGroup',
            compile: function (element, attr, transclude) {
                return function link(scope, element, attr, accordionGroupCtrl) {
                    // Pass the heading to the accordion-group controller
                    // so that it can be transcluded into the right place in the template
                    // [The second parameter to transclude causes the elements to be cloned so that they work in ng-repeat]
                    accordionGroupCtrl.setHeading(transclude(scope, function () {
                    }));
                };
            }
        };
    })

// Use in the accordion-group template to indicate where you want the heading to be transcluded
// You must provide the property on the accordion-group controller that will hold the transcluded element
// <div class="accordion-group">
//   <div class="accordion-heading" ><a ... accordion-transclude="heading">...</a></div>
//   ...
// </div>
    .directive('accordionTransclude', function () {
        return {
            require: '^accordionGroup',
            link: function (scope, element, attr, controller) {
                scope.$watch(function () {
                    return controller[attr.accordionTransclude];
                }, function (heading) {
                    if (heading) {
                        element.html('');
                        element.append(heading);
                    }
                });
            }
        };
    });

angular.module("ui.bootstrap.alert", []).directive('alert', function () {
    return {
        restrict: 'EA',
        templateUrl: 'template/alert/alert.html',
        transclude: true,
        replace: true,
        scope: {
            type: '=',
            close: '&'
        },
        link: function (scope, iElement, iAttrs, controller) {
            scope.closeable = "close" in iAttrs;
        }
    };
});

angular.module('ui.bootstrap.bindHtml', [])

    .directive('bindHtmlUnsafe', function () {
        return function (scope, element, attr) {
            element.addClass('ng-binding').data('$binding', attr.bindHtmlUnsafe);
            scope.$watch(attr.bindHtmlUnsafe, function bindHtmlUnsafeWatchAction(value) {
                element.html(value || '');
            });
        };
    });
angular.module('ui.bootstrap.buttons', [])

    .constant('buttonConfig', {
        activeClass: 'active',
        toggleEvent: 'click'
    })

    .directive('btnRadio', ['buttonConfig', function (buttonConfig) {
        var activeClass = buttonConfig.activeClass || 'active';
        var toggleEvent = buttonConfig.toggleEvent || 'click';

        return {

            require: 'ngModel',
            link: function (scope, element, attrs, ngModelCtrl) {

                //model -> UI
                ngModelCtrl.$render = function () {
                    element.toggleClass(activeClass, angular.equals(ngModelCtrl.$modelValue, scope.$eval(attrs.btnRadio)));
                };

                //ui->model
                element.bind(toggleEvent, function () {
                    if (!element.hasClass(activeClass)) {
                        scope.$apply(function () {
                            ngModelCtrl.$setViewValue(scope.$eval(attrs.btnRadio));
                            ngModelCtrl.$render();
                        });
                    }
                });
            }
        };
    }])

    .directive('btnCheckbox', ['buttonConfig', function (buttonConfig) {

        var activeClass = buttonConfig.activeClass || 'active';
        var toggleEvent = buttonConfig.toggleEvent || 'click';

        return {
            require: 'ngModel',
            link: function (scope, element, attrs, ngModelCtrl) {

                function getTrueValue() {
                    var trueValue = scope.$eval(attrs.btnCheckboxTrue);
                    return angular.isDefined(trueValue) ? trueValue : true;
                }

                function getFalseValue() {
                    var falseValue = scope.$eval(attrs.btnCheckboxFalse);
                    return angular.isDefined(falseValue) ? falseValue : false;
                }

                //model -> UI
                ngModelCtrl.$render = function () {
                    element.toggleClass(activeClass, angular.equals(ngModelCtrl.$modelValue, getTrueValue()));
                };

                //ui->model
                element.bind(toggleEvent, function () {
                    scope.$apply(function () {
                        ngModelCtrl.$setViewValue(element.hasClass(activeClass) ? getFalseValue() : getTrueValue());
                        ngModelCtrl.$render();
                    });
                });
            }
        };
    }]);

angular.module('ui.bootstrap.position', [])

/**
 * A set of utility methods that can be use to retrieve position of DOM elements.
 * It is meant to be used where we need to absolute-position DOM elements in
 * relation to other, existing elements (this is the case for tooltips, popovers,
 * typeahead suggestions etc.).
 */
    .factory('$position', ['$document', '$window', function ($document, $window) {

        function getStyle(el, cssprop) {
            if (el.currentStyle) { //IE
                return el.currentStyle[cssprop];
            } else if ($window.getComputedStyle) {
                return $window.getComputedStyle(el)[cssprop];
            }
            // finally try and get inline style
            return el.style[cssprop];
        }

        /**
         * Checks if a given element is statically positioned
         * @param element - raw DOM element
         */
        function isStaticPositioned(element) {
            return (getStyle(element, "position") || 'static' ) === 'static';
        }

        /**
         * returns the closest, non-statically positioned parentOffset of a given element
         * @param element
         */
        var parentOffsetEl = function (element) {
            var docDomEl = $document[0];
            var offsetParent = element.offsetParent || docDomEl;
            while (offsetParent && offsetParent !== docDomEl && isStaticPositioned(offsetParent)) {
                offsetParent = offsetParent.offsetParent;
            }
            return offsetParent || docDomEl;
        };

        return {
            /**
             * Provides read-only equivalent of jQuery's position function:
             * http://api.jquery.com/position/
             */
            position: function (element) {
                var elBCR = this.offset(element);
                var offsetParentBCR = { top: 0, left: 0 };
                var offsetParentEl = parentOffsetEl(element[0]);
                if (offsetParentEl !== $document[0]) {
                    offsetParentBCR = this.offset(angular.element(offsetParentEl));
                    offsetParentBCR.top += offsetParentEl.clientTop - offsetParentEl.scrollTop;
                    offsetParentBCR.left += offsetParentEl.clientLeft - offsetParentEl.scrollLeft;
                }

                return {
                    width: element.prop('offsetWidth'),
                    height: element.prop('offsetHeight'),
                    top: elBCR.top - offsetParentBCR.top,
                    left: elBCR.left - offsetParentBCR.left
                };
            },

            /**
             * Provides read-only equivalent of jQuery's offset function:
             * http://api.jquery.com/offset/
             */
            offset: function (element) {
                var boundingClientRect = element[0].getBoundingClientRect();
                return {
                    width: element.prop('offsetWidth'),
                    height: element.prop('offsetHeight'),
                    top: boundingClientRect.top + ($window.pageYOffset || $document[0].body.scrollTop || $document[0].documentElement.scrollTop),
                    left: boundingClientRect.left + ($window.pageXOffset || $document[0].body.scrollLeft || $document[0].documentElement.scrollLeft)
                };
            }
        };
    }]);

/*
 * dropdownToggle - Provides dropdown menu functionality in place of bootstrap js
 * @restrict class or attribute
 * @example:
 <li class="dropdown">
 <a class="dropdown-toggle">My Dropdown Menu</a>
 <ul class="dropdown-menu">
 <li ng-repeat="choice in dropChoices">
 <a ng-href="{{choice.href}}">{{choice.text}}</a>
 </li>
 </ul>
 </li>
 */

angular.module('ui.bootstrap.dropdownToggle', []).directive('dropdownToggle', ['$document', '$location', function ($document, $location) {
    var openElement = null,
        closeMenu = angular.noop;
    return {
        restrict: 'CA',
        link: function (scope, element, attrs) {
            scope.$watch('$location.path', function () {
                closeMenu();
            });
            element.parent().bind('click', function () {
                closeMenu();
            });
            element.bind('click', function (event) {

                var elementWasOpen = (element === openElement);

                event.preventDefault();
                event.stopPropagation();

                if (!!openElement) {
                    closeMenu();
                }

                if (!elementWasOpen) {
                    element.parent().addClass('open');
                    openElement = element;
                    closeMenu = function (event) {
                        if (event) {
                            event.preventDefault();
                            event.stopPropagation();
                        }
                        $document.unbind('click', closeMenu);
                        element.parent().removeClass('open');
                        closeMenu = angular.noop;
                        openElement = null;
                    };
                    $document.bind('click', closeMenu);
                }
            });
        }
    };
}]);
angular.module('ui.bootstrap.modal', [])

/**
 * A helper, internal data structure that acts as a map but also allows getting / removing
 * elements in the LIFO order
 */
    .factory('$$stackedMap', function () {
        return {
            createNew: function () {
                var stack = [];

                return {
                    add: function (key, value) {
                        stack.push({
                            key: key,
                            value: value
                        });
                    },
                    get: function (key) {
                        for (var i = 0; i < stack.length; i++) {
                            if (key === stack[i].key) {
                                return stack[i];
                            }
                        }
                    },
                    keys: function () {
                        var keys = [];
                        for (var i = 0; i < stack.length; i++) {
                            keys.push(stack[i].key);
                        }
                        return keys;
                    },
                    top: function () {
                        return stack[stack.length - 1];
                    },
                    remove: function (key) {
                        var idx = -1;
                        for (var i = 0; i < stack.length; i++) {
                            if (key === stack[i].key) {
                                idx = i;
                                break;
                            }
                        }
                        return stack.splice(idx, 1)[0];
                    },
                    removeTop: function () {
                        return stack.splice(stack.length - 1, 1)[0];
                    },
                    length: function () {
                        return stack.length;
                    }
                };
            }
        };
    })

/**
 * A helper directive for the $modal service. It creates a backdrop element.
 */
    .directive('modalBackdrop', ['$modalStack', '$timeout', function ($modalStack, $timeout) {
        return {
            restrict: 'EA',
            replace: true,
            templateUrl: 'template/modal/backdrop.html',
            link: function (scope, element, attrs) {

                //trigger CSS transitions
                $timeout(function () {
                    scope.animate = true;
                });

                scope.close = function (evt) {
                    var modal = $modalStack.getTop();
                    if (modal && modal.value.backdrop && modal.value.backdrop !== 'static') {
                        evt.preventDefault();
                        evt.stopPropagation();
                        $modalStack.dismiss(modal.key, 'backdrop click');
                    }
                };
            }
        };
    }])

    .directive('modalWindow', ['$timeout', function ($timeout) {
        return {
            restrict: 'EA',
            scope: {
                index: '@'
            },
            replace: true,
            transclude: true,
            templateUrl: 'template/modal/window.html',
            link: function (scope, element, attrs) {
                scope.windowClass = attrs.windowClass || '';

                //trigger CSS transitions
                $timeout(function () {
                    scope.animate = true;
                });
            }
        };
    }])

    .factory('$modalStack', ['$document', '$compile', '$rootScope', '$$stackedMap',
        function ($document, $compile, $rootScope, $$stackedMap) {

            var backdropjqLiteEl, backdropDomEl;
            var backdropScope = $rootScope.$new(true);
            var body = $document.find('body').eq(0);
            var openedWindows = $$stackedMap.createNew();
            var $modalStack = {};

            function backdropIndex() {
                var topBackdropIndex = -1;
                var opened = openedWindows.keys();
                for (var i = 0; i < opened.length; i++) {
                    if (openedWindows.get(opened[i]).value.backdrop) {
                        topBackdropIndex = i;
                    }
                }
                return topBackdropIndex;
            }

            $rootScope.$watch(backdropIndex, function (newBackdropIndex) {
                backdropScope.index = newBackdropIndex;
            });

            function removeModalWindow(modalInstance) {

                var modalWindow = openedWindows.get(modalInstance).value;

                //clean up the stack
                openedWindows.remove(modalInstance);

                //remove window DOM element
                modalWindow.modalDomEl.remove();

                //remove backdrop if no longer needed
                if (backdropIndex() === -1) {
                    backdropDomEl.remove();
                    backdropDomEl = undefined;
                }

                //destroy scope
                modalWindow.modalScope.$destroy();
            }

            $document.bind('keydown', function (evt) {
                var modal;

                if (evt.which === 27) {
                    modal = openedWindows.top();
                    if (modal && modal.value.keyboard) {
                        $rootScope.$apply(function () {
                            $modalStack.dismiss(modal.key);
                        });
                    }
                }
            });

            $modalStack.open = function (modalInstance, modal) {

                openedWindows.add(modalInstance, {
                    deferred: modal.deferred,
                    modalScope: modal.scope,
                    backdrop: modal.backdrop,
                    keyboard: modal.keyboard
                });

                var angularDomEl = angular.element('<div modal-window></div>');
                angularDomEl.attr('window-class', modal.windowClass);
                angularDomEl.attr('index', openedWindows.length() - 1);
                angularDomEl.html(modal.content);

                var modalDomEl = $compile(angularDomEl)(modal.scope);
                openedWindows.top().value.modalDomEl = modalDomEl;
                body.append(modalDomEl);

                if (backdropIndex() >= 0 && !backdropDomEl) {
                    backdropjqLiteEl = angular.element('<div modal-backdrop></div>');
                    backdropDomEl = $compile(backdropjqLiteEl)(backdropScope);
                    body.append(backdropDomEl);
                }
            };

            $modalStack.close = function (modalInstance, result) {
                var modal = openedWindows.get(modalInstance);
                if (modal) {
                    modal.value.deferred.resolve(result);
                    removeModalWindow(modalInstance);
                }
            };

            $modalStack.dismiss = function (modalInstance, reason) {
                var modalWindow = openedWindows.get(modalInstance).value;
                if (modalWindow) {
                    modalWindow.deferred.reject(reason);
                    removeModalWindow(modalInstance);
                }
            };

            $modalStack.getTop = function () {
                return openedWindows.top();
            };

            return $modalStack;
        }])

    .provider('$modal', function () {

        var $modalProvider = {
            options: {
                backdrop: true, //can be also false or 'static'
                keyboard: true
            },
            $get: ['$injector', '$rootScope', '$q', '$http', '$templateCache', '$controller', '$modalStack',
                function ($injector, $rootScope, $q, $http, $templateCache, $controller, $modalStack) {

                    var $modal = {};

                    function getTemplatePromise(options) {
                        return options.template ? $q.when(options.template) :
                            $http.get(options.templateUrl, {cache: $templateCache}).then(function (result) {
                                return result.data;
                            });
                    }

                    function getResolvePromises(resolves) {
                        var promisesArr = [];
                        angular.forEach(resolves, function (value, key) {
                            if (angular.isFunction(value) || angular.isArray(value)) {
                                promisesArr.push($q.when($injector.invoke(value)));
                            }
                        });
                        return promisesArr;
                    }

                    $modal.open = function (modalOptions) {

                        var modalResultDeferred = $q.defer();
                        var modalOpenedDeferred = $q.defer();

                        //prepare an instance of a modal to be injected into controllers and returned to a caller
                        var modalInstance = {
                            result: modalResultDeferred.promise,
                            opened: modalOpenedDeferred.promise,
                            close: function (result) {
                                $modalStack.close(modalInstance, result);
                            },
                            dismiss: function (reason) {
                                $modalStack.dismiss(modalInstance, reason);
                            }
                        };

                        //merge and clean up options
                        modalOptions = angular.extend({}, $modalProvider.options, modalOptions);
                        modalOptions.resolve = modalOptions.resolve || {};

                        //verify options
                        if (!modalOptions.template && !modalOptions.templateUrl) {
                            throw new Error('One of template or templateUrl options is required.');
                        }

                        var templateAndResolvePromise =
                            $q.all([getTemplatePromise(modalOptions)].concat(getResolvePromises(modalOptions.resolve)));


                        templateAndResolvePromise.then(function resolveSuccess(tplAndVars) {

                            var modalScope = (modalOptions.scope || $rootScope).$new();
                            modalScope.$close = modalInstance.close;
                            modalScope.$dismiss = modalInstance.dismiss;

                            var ctrlInstance, ctrlLocals = {};
                            var resolveIter = 1;

                            //controllers
                            if (modalOptions.controller) {
                                ctrlLocals.$scope = modalScope;
                                ctrlLocals.$modalInstance = modalInstance;
                                angular.forEach(modalOptions.resolve, function (value, key) {
                                    ctrlLocals[key] = tplAndVars[resolveIter++];
                                });

                                ctrlInstance = $controller(modalOptions.controller, ctrlLocals);
                            }

                            $modalStack.open(modalInstance, {
                                scope: modalScope,
                                deferred: modalResultDeferred,
                                content: tplAndVars[0],
                                backdrop: modalOptions.backdrop,
                                keyboard: modalOptions.keyboard,
                                windowClass: modalOptions.windowClass
                            });

                        }, function resolveError(reason) {
                            modalResultDeferred.reject(reason);
                        });

                        templateAndResolvePromise.then(function () {
                            modalOpenedDeferred.resolve(true);
                        }, function () {
                            modalOpenedDeferred.reject(false);
                        });

                        return modalInstance;
                    };

                    return $modal;
                }]
        };

        return $modalProvider;
    });
angular.module('ui.bootstrap.pagination', [])

    .controller('PaginationController', ['$scope', '$attrs', '$parse', '$interpolate', function ($scope, $attrs, $parse, $interpolate) {
        var self = this;

        this.init = function (defaultItemsPerPage) {
            if ($attrs.itemsPerPage) {
                $scope.$parent.$watch($parse($attrs.itemsPerPage), function (value) {
                    self.itemsPerPage = parseInt(value, 10);
                    $scope.totalPages = self.calculateTotalPages();
                });
            } else {
                this.itemsPerPage = defaultItemsPerPage;
            }
        };

        this.noPrevious = function () {
            return this.page === 1;
        };
        this.noNext = function () {
            return this.page === $scope.totalPages;
        };

        this.isActive = function (page) {
            return this.page === page;
        };

        this.calculateTotalPages = function () {
            return this.itemsPerPage < 1 ? 1 : Math.ceil($scope.totalItems / this.itemsPerPage);
        };

        this.getAttributeValue = function (attribute, defaultValue, interpolate) {
            return angular.isDefined(attribute) ? (interpolate ? $interpolate(attribute)($scope.$parent) : $scope.$parent.$eval(attribute)) : defaultValue;
        };

        this.render = function () {
            this.page = parseInt($scope.page, 10) || 1;
            $scope.pages = this.getPages(this.page, $scope.totalPages);
        };

        $scope.selectPage = function (page) {
            if (!self.isActive(page) && page > 0 && page <= $scope.totalPages) {
                $scope.page = page;
                $scope.onSelectPage({ page: page });
            }
        };

        $scope.$watch('totalItems', function () {
            $scope.totalPages = self.calculateTotalPages();
        });

        $scope.$watch('totalPages', function (value) {
            if ($attrs.numPages) {
                $scope.numPages = value; // Readonly variable
            }

            if (self.page > value) {
                $scope.selectPage(value);
            } else {
                self.render();
            }
        });

        $scope.$watch('page', function () {
            self.render();
        });
    }])

    .constant('paginationConfig', {
        itemsPerPage: 10,
        boundaryLinks: false,
        directionLinks: true,
        firstText: 'First',
        previousText: 'Previous',
        nextText: 'Next',
        lastText: 'Last',
        rotate: true
    })

    .directive('pagination', ['$parse', 'paginationConfig', function ($parse, config) {
        return {
            restrict: 'EA',
            scope: {
                page: '=',
                totalItems: '=',
                onSelectPage: ' &',
                numPages: '='
            },
            controller: 'PaginationController',
            templateUrl: 'template/pagination/pagination.html',
            replace: true,
            link: function (scope, element, attrs, paginationCtrl) {

                // Setup configuration parameters
                var maxSize,
                    boundaryLinks = paginationCtrl.getAttributeValue(attrs.boundaryLinks, config.boundaryLinks),
                    directionLinks = paginationCtrl.getAttributeValue(attrs.directionLinks, config.directionLinks),
                    firstText = paginationCtrl.getAttributeValue(attrs.firstText, config.firstText, true),
                    previousText = paginationCtrl.getAttributeValue(attrs.previousText, config.previousText, true),
                    nextText = paginationCtrl.getAttributeValue(attrs.nextText, config.nextText, true),
                    lastText = paginationCtrl.getAttributeValue(attrs.lastText, config.lastText, true),
                    rotate = paginationCtrl.getAttributeValue(attrs.rotate, config.rotate);

                paginationCtrl.init(config.itemsPerPage);

                if (attrs.maxSize) {
                    scope.$parent.$watch($parse(attrs.maxSize), function (value) {
                        maxSize = parseInt(value, 10);
                        paginationCtrl.render();
                    });
                }

                // Create page object used in template
                function makePage(number, text, isActive, isDisabled) {
                    return {
                        number: number,
                        text: text,
                        active: isActive,
                        disabled: isDisabled
                    };
                }

                paginationCtrl.getPages = function (currentPage, totalPages) {
                    var pages = [];

                    // Default page limits
                    var startPage = 1, endPage = totalPages;
                    var isMaxSized = ( angular.isDefined(maxSize) && maxSize < totalPages );

                    // recompute if maxSize
                    if (isMaxSized) {
                        if (rotate) {
                            // Current page is displayed in the middle of the visible ones
                            startPage = Math.max(currentPage - Math.floor(maxSize / 2), 1);
                            endPage = startPage + maxSize - 1;

                            // Adjust if limit is exceeded
                            if (endPage > totalPages) {
                                endPage = totalPages;
                                startPage = endPage - maxSize + 1;
                            }
                        } else {
                            // Visible pages are paginated with maxSize
                            startPage = ((Math.ceil(currentPage / maxSize) - 1) * maxSize) + 1;

                            // Adjust last page if limit is exceeded
                            endPage = Math.min(startPage + maxSize - 1, totalPages);
                        }
                    }

                    // Add page number links
                    for (var number = startPage; number <= endPage; number++) {
                        var page = makePage(number, number, paginationCtrl.isActive(number), false);
                        pages.push(page);
                    }

                    // Add links to move between page sets
                    if (isMaxSized && !rotate) {
                        if (startPage > 1) {
                            var previousPageSet = makePage(startPage - 1, '...', false, false);
                            pages.unshift(previousPageSet);
                        }

                        if (endPage < totalPages) {
                            var nextPageSet = makePage(endPage + 1, '...', false, false);
                            pages.push(nextPageSet);
                        }
                    }

                    // Add previous & next links
                    if (directionLinks) {
                        var previousPage = makePage(currentPage - 1, previousText, false, paginationCtrl.noPrevious());
                        pages.unshift(previousPage);

                        var nextPage = makePage(currentPage + 1, nextText, false, paginationCtrl.noNext());
                        pages.push(nextPage);
                    }

                    // Add first & last links
                    if (boundaryLinks) {
                        var firstPage = makePage(1, firstText, false, paginationCtrl.noPrevious());
                        pages.unshift(firstPage);

                        var lastPage = makePage(totalPages, lastText, false, paginationCtrl.noNext());
                        pages.push(lastPage);
                    }

                    return pages;
                };
            }
        };
    }])

    .constant('pagerConfig', {
        itemsPerPage: 10,
        previousText: '« Previous',
        nextText: 'Next »',
        align: true
    })

    .directive('pager', ['pagerConfig', function (config) {
        return {
            restrict: 'EA',
            scope: {
                page: '=',
                totalItems: '=',
                onSelectPage: ' &',
                numPages: '='
            },
            controller: 'PaginationController',
            templateUrl: 'template/pagination/pager.html',
            replace: true,
            link: function (scope, element, attrs, paginationCtrl) {

                // Setup configuration parameters
                var previousText = paginationCtrl.getAttributeValue(attrs.previousText, config.previousText, true),
                    nextText = paginationCtrl.getAttributeValue(attrs.nextText, config.nextText, true),
                    align = paginationCtrl.getAttributeValue(attrs.align, config.align);

                paginationCtrl.init(config.itemsPerPage);

                // Create page object used in template
                function makePage(number, text, isDisabled, isPrevious, isNext) {
                    return {
                        number: number,
                        text: text,
                        disabled: isDisabled,
                        previous: ( align && isPrevious ),
                        next: ( align && isNext )
                    };
                }

                paginationCtrl.getPages = function (currentPage) {
                    return [
                        makePage(currentPage - 1, previousText, paginationCtrl.noPrevious(), true, false),
                        makePage(currentPage + 1, nextText, paginationCtrl.noNext(), false, true)
                    ];
                };
            }
        };
    }]);

/**
 * The following features are still outstanding: animation as a
 * function, placement as a function, inside, support for more triggers than
 * just mouse enter/leave, html tooltips, and selector delegation.
 */
angular.module('ui.bootstrap.tooltip', [ 'ui.bootstrap.position', 'ui.bootstrap.bindHtml' ])

/**
 * The $tooltip service creates tooltip- and popover-like directives as well as
 * houses global options for them.
 */
    .provider('$tooltip', function () {
        // The default options tooltip and popover.
        var defaultOptions = {
            placement: 'top',
            animation: true,
            popupDelay: 0
        };

        // Default hide triggers for each show trigger
        var triggerMap = {
            'mouseenter': 'mouseleave',
            'click': 'click',
            'focus': 'blur'
        };

        // The options specified to the provider globally.
        var globalOptions = {};

        /**
         * `options({})` allows global configuration of all tooltips in the
         * application.
         *
         *   var app = angular.module( 'App', ['ui.bootstrap.tooltip'], function( $tooltipProvider ) {
   *     // place tooltips left instead of top by default
   *     $tooltipProvider.options( { placement: 'left' } );
   *   });
         */
        this.options = function (value) {
            angular.extend(globalOptions, value);
        };

        /**
         * This allows you to extend the set of trigger mappings available. E.g.:
         *
         *   $tooltipProvider.setTriggers( 'openTrigger': 'closeTrigger' );
         */
        this.setTriggers = function setTriggers(triggers) {
            angular.extend(triggerMap, triggers);
        };

        /**
         * This is a helper function for translating camel-case to snake-case.
         */
        function snake_case(name) {
            var regexp = /[A-Z]/g;
            var separator = '-';
            return name.replace(regexp, function (letter, pos) {
                return (pos ? separator : '') + letter.toLowerCase();
            });
        }

        /**
         * Returns the actual instance of the $tooltip service.
         * TODO support multiple triggers
         */
        this.$get = [ '$window', '$compile', '$timeout', '$parse', '$document', '$position', '$interpolate', function ($window, $compile, $timeout, $parse, $document, $position, $interpolate) {
            return function $tooltip(type, prefix, defaultTriggerShow) {
                var options = angular.extend({}, defaultOptions, globalOptions);

                /**
                 * Returns an object of show and hide triggers.
                 *
                 * If a trigger is supplied,
                 * it is used to show the tooltip; otherwise, it will use the `trigger`
                 * option passed to the `$tooltipProvider.options` method; else it will
                 * default to the trigger supplied to this directive factory.
                 *
                 * The hide trigger is based on the show trigger. If the `trigger` option
                 * was passed to the `$tooltipProvider.options` method, it will use the
                 * mapped trigger from `triggerMap` or the passed trigger if the map is
                 * undefined; otherwise, it uses the `triggerMap` value of the show
                 * trigger; else it will just use the show trigger.
                 */
                function getTriggers(trigger) {
                    var show = trigger || options.trigger || defaultTriggerShow;
                    var hide = triggerMap[show] || show;
                    return {
                        show: show,
                        hide: hide
                    };
                }

                var directiveName = snake_case(type);

                var startSym = $interpolate.startSymbol();
                var endSym = $interpolate.endSymbol();
                var template =
                    '<' + directiveName + '-popup ' +
                        'title="' + startSym + 'tt_title' + endSym + '" ' +
                        'content="' + startSym + 'tt_content' + endSym + '" ' +
                        'placement="' + startSym + 'tt_placement' + endSym + '" ' +
                        'animation="tt_animation()" ' +
                        'is-open="tt_isOpen"' +
                        '>' +
                        '</' + directiveName + '-popup>';

                return {
                    restrict: 'EA',
                    scope: true,
                    link: function link(scope, element, attrs) {
                        var tooltip = $compile(template)(scope);
                        var transitionTimeout;
                        var popupTimeout;
                        var $body;
                        var appendToBody = angular.isDefined(options.appendToBody) ? options.appendToBody : false;
                        var triggers = getTriggers(undefined);
                        var hasRegisteredTriggers = false;

                        // By default, the tooltip is not open.
                        // TODO add ability to start tooltip opened
                        scope.tt_isOpen = false;

                        function toggleTooltipBind() {
                            if (!scope.tt_isOpen) {
                                showTooltipBind();
                            } else {
                                hideTooltipBind();
                            }
                        }

                        // Show the tooltip with delay if specified, otherwise show it immediately
                        function showTooltipBind() {
                            if (scope.tt_popupDelay) {
                                popupTimeout = $timeout(show, scope.tt_popupDelay);
                            } else {
                                scope.$apply(show);
                            }
                        }

                        function hideTooltipBind() {
                            scope.$apply(function () {
                                hide();
                            });
                        }

                        // Show the tooltip popup element.
                        function show() {
                            var position,
                                ttWidth,
                                ttHeight,
                                ttPosition;

                            // Don't show empty tooltips.
                            if (!scope.tt_content) {
                                return;
                            }

                            // If there is a pending remove transition, we must cancel it, lest the
                            // tooltip be mysteriously removed.
                            if (transitionTimeout) {
                                $timeout.cancel(transitionTimeout);
                            }

                            // Set the initial positioning.
                            tooltip.css({ top: 0, left: 0, display: 'block' });

                            // Now we add it to the DOM because need some info about it. But it's not
                            // visible yet anyway.
                            if (appendToBody) {
                                $body = $body || $document.find('body');
                                $body.append(tooltip);
                            } else {
                                element.after(tooltip);
                            }

                            // Get the position of the directive element.
                            position = appendToBody ? $position.offset(element) : $position.position(element);

                            // Get the height and width of the tooltip so we can center it.
                            ttWidth = tooltip.prop('offsetWidth');
                            ttHeight = tooltip.prop('offsetHeight');

                            // Calculate the tooltip's top and left coordinates to center it with
                            // this directive.
                            switch (scope.tt_placement) {
                                case 'right':
                                    ttPosition = {
                                        top: position.top + position.height / 2 - ttHeight / 2,
                                        left: position.left + position.width
                                    };
                                    break;
                                case 'bottom':
                                    ttPosition = {
                                        top: position.top + position.height,
                                        left: position.left + position.width / 2 - ttWidth / 2
                                    };
                                    break;
                                case 'left':
                                    ttPosition = {
                                        top: position.top + position.height / 2 - ttHeight / 2,
                                        left: position.left - ttWidth
                                    };
                                    break;
                                default:
                                    ttPosition = {
                                        top: position.top - ttHeight,
                                        left: position.left + position.width / 2 - ttWidth / 2
                                    };
                                    break;
                            }

                            ttPosition.top += 'px';
                            ttPosition.left += 'px';

                            // Now set the calculated positioning.
                            tooltip.css(ttPosition);

                            // And show the tooltip.
                            scope.tt_isOpen = true;
                        }

                        // Hide the tooltip popup element.
                        function hide() {
                            // First things first: we don't show it anymore.
                            scope.tt_isOpen = false;

                            //if tooltip is going to be shown after delay, we must cancel this
                            $timeout.cancel(popupTimeout);

                            // And now we remove it from the DOM. However, if we have animation, we
                            // need to wait for it to expire beforehand.
                            // FIXME: this is a placeholder for a port of the transitions library.
                            if (angular.isDefined(scope.tt_animation) && scope.tt_animation()) {
                                transitionTimeout = $timeout(function () {
                                    tooltip.remove();
                                }, 500);
                            } else {
                                tooltip.remove();
                            }
                        }

                        /**
                         * Observe the relevant attributes.
                         */
                        attrs.$observe(type, function (val) {
                            scope.tt_content = val;
                        });

                        attrs.$observe(prefix + 'Title', function (val) {
                            scope.tt_title = val;
                        });

                        attrs.$observe(prefix + 'Placement', function (val) {
                            scope.tt_placement = angular.isDefined(val) ? val : options.placement;
                        });

                        attrs.$observe(prefix + 'Animation', function (val) {
                            scope.tt_animation = angular.isDefined(val) ? $parse(val) : function () {
                                return options.animation;
                            };
                        });

                        attrs.$observe(prefix + 'PopupDelay', function (val) {
                            var delay = parseInt(val, 10);
                            scope.tt_popupDelay = !isNaN(delay) ? delay : options.popupDelay;
                        });

                        attrs.$observe(prefix + 'Trigger', function (val) {

                            if (hasRegisteredTriggers) {
                                element.unbind(triggers.show, showTooltipBind);
                                element.unbind(triggers.hide, hideTooltipBind);
                            }

                            triggers = getTriggers(val);

                            if (triggers.show === triggers.hide) {
                                element.bind(triggers.show, toggleTooltipBind);
                            } else {
                                element.bind(triggers.show, showTooltipBind);
                                element.bind(triggers.hide, hideTooltipBind);
                            }

                            hasRegisteredTriggers = true;
                        });

                        attrs.$observe(prefix + 'AppendToBody', function (val) {
                            appendToBody = angular.isDefined(val) ? $parse(val)(scope) : appendToBody;
                        });

                        // if a tooltip is attached to <body> we need to remove it on
                        // location change as its parent scope will probably not be destroyed
                        // by the change.
                        if (appendToBody) {
                            scope.$on('$locationChangeSuccess', function closeTooltipOnLocationChangeSuccess() {
                                if (scope.tt_isOpen) {
                                    hide();
                                }
                            });
                        }

                        // Make sure tooltip is destroyed and removed.
                        scope.$on('$destroy', function onDestroyTooltip() {
                            if (scope.tt_isOpen) {
                                hide();
                            } else {
                                tooltip.remove();
                            }
                        });
                    }
                };
            };
        }];
    })

    .directive('tooltipPopup', function () {
        return {
            restrict: 'E',
            replace: true,
            scope: { content: '@', placement: '@', animation: '&', isOpen: '&' },
            templateUrl: 'template/tooltip/tooltip-popup.html'
        };
    })

    .directive('tooltip', [ '$tooltip', function ($tooltip) {
        return $tooltip('tooltip', 'tooltip', 'mouseenter');
    }])

    .directive('tooltipHtmlUnsafePopup', function () {
        return {
            restrict: 'E',
            replace: true,
            scope: { content: '@', placement: '@', animation: '&', isOpen: '&' },
            templateUrl: 'template/tooltip/tooltip-html-unsafe-popup.html'
        };
    })

    .directive('tooltipHtmlUnsafe', [ '$tooltip', function ($tooltip) {
        return $tooltip('tooltipHtmlUnsafe', 'tooltip', 'mouseenter');
    }]);

/**
 * The following features are still outstanding: popup delay, animation as a
 * function, placement as a function, inside, support for more triggers than
 * just mouse enter/leave, html popovers, and selector delegatation.
 */
angular.module('ui.bootstrap.popover', [ 'ui.bootstrap.tooltip' ])
    .directive('popoverPopup', function () {
        return {
            restrict: 'EA',
            replace: true,
            scope: { title: '@', content: '@', placement: '@', animation: '&', isOpen: '&' },
            templateUrl: 'template/popover/popover.html'
        };
    })
    .directive('popover', [ '$compile', '$timeout', '$parse', '$window', '$tooltip', function ($compile, $timeout, $parse, $window, $tooltip) {
        return $tooltip('popover', 'popover', 'click');
    }]);


angular.module('ui.bootstrap.progressbar', ['ui.bootstrap.transition'])

    .constant('progressConfig', {
        animate: true,
        autoType: false,
        stackedTypes: ['success', 'info', 'warning', 'danger']
    })

    .controller('ProgressBarController', ['$scope', '$attrs', 'progressConfig', function ($scope, $attrs, progressConfig) {

        // Whether bar transitions should be animated
        var animate = angular.isDefined($attrs.animate) ? $scope.$eval($attrs.animate) : progressConfig.animate;
        var autoType = angular.isDefined($attrs.autoType) ? $scope.$eval($attrs.autoType) : progressConfig.autoType;
        var stackedTypes = angular.isDefined($attrs.stackedTypes) ? $scope.$eval('[' + $attrs.stackedTypes + ']') : progressConfig.stackedTypes;

        // Create bar object
        this.makeBar = function (newBar, oldBar, index) {
            var newValue = (angular.isObject(newBar)) ? newBar.value : (newBar || 0);
            var oldValue = (angular.isObject(oldBar)) ? oldBar.value : (oldBar || 0);
            var type = (angular.isObject(newBar) && angular.isDefined(newBar.type)) ? newBar.type : (autoType) ? getStackedType(index || 0) : null;

            return {
                from: oldValue,
                to: newValue,
                type: type,
                animate: animate
            };
        };

        function getStackedType(index) {
            return stackedTypes[index];
        }

        this.addBar = function (bar) {
            $scope.bars.push(bar);
            $scope.totalPercent += bar.to;
        };

        this.clearBars = function () {
            $scope.bars = [];
            $scope.totalPercent = 0;
        };
        this.clearBars();
    }])

    .directive('progress', function () {
        return {
            restrict: 'EA',
            replace: true,
            controller: 'ProgressBarController',
            scope: {
                value: '=percent',
                onFull: '&',
                onEmpty: '&'
            },
            templateUrl: 'template/progressbar/progress.html',
            link: function (scope, element, attrs, controller) {
                scope.$watch('value', function (newValue, oldValue) {
                    controller.clearBars();

                    if (angular.isArray(newValue)) {
                        // Stacked progress bar
                        for (var i = 0, n = newValue.length; i < n; i++) {
                            controller.addBar(controller.makeBar(newValue[i], oldValue[i], i));
                        }
                    } else {
                        // Simple bar
                        controller.addBar(controller.makeBar(newValue, oldValue));
                    }
                }, true);

                // Total percent listeners
                scope.$watch('totalPercent', function (value) {
                    if (value >= 100) {
                        scope.onFull();
                    } else if (value <= 0) {
                        scope.onEmpty();
                    }
                }, true);
            }
        };
    })

    .directive('progressbar', ['$transition', function ($transition) {
        return {
            restrict: 'EA',
            replace: true,
            scope: {
                width: '=',
                old: '=',
                type: '=',
                animate: '='
            },
            templateUrl: 'template/progressbar/bar.html',
            link: function (scope, element) {
                scope.$watch('width', function (value) {
                    if (scope.animate) {
                        element.css('width', scope.old + '%');
                        $transition(element, {width: value + '%'});
                    } else {
                        element.css('width', value + '%');
                    }
                });
            }
        };
    }]);
angular.module('ui.bootstrap.rating', [])

    .constant('ratingConfig', {
        max: 5,
        stateOn: null,
        stateOff: null
    })

    .controller('RatingController', ['$scope', '$attrs', '$parse', 'ratingConfig', function ($scope, $attrs, $parse, ratingConfig) {

        this.maxRange = angular.isDefined($attrs.max) ? $scope.$parent.$eval($attrs.max) : ratingConfig.max;
        this.stateOn = angular.isDefined($attrs.stateOn) ? $scope.$parent.$eval($attrs.stateOn) : ratingConfig.stateOn;
        this.stateOff = angular.isDefined($attrs.stateOff) ? $scope.$parent.$eval($attrs.stateOff) : ratingConfig.stateOff;

        this.createDefaultRange = function (len) {
            var defaultStateObject = {
                stateOn: this.stateOn,
                stateOff: this.stateOff
            };

            var states = new Array(len);
            for (var i = 0; i < len; i++) {
                states[i] = defaultStateObject;
            }
            return states;
        };

        this.normalizeRange = function (states) {
            for (var i = 0, n = states.length; i < n; i++) {
                states[i].stateOn = states[i].stateOn || this.stateOn;
                states[i].stateOff = states[i].stateOff || this.stateOff;
            }
            return states;
        };

        // Get objects used in template
        $scope.range = angular.isDefined($attrs.ratingStates) ? this.normalizeRange(angular.copy($scope.$parent.$eval($attrs.ratingStates))) : this.createDefaultRange(this.maxRange);

        $scope.rate = function (value) {
            if ($scope.readonly || $scope.value === value) {
                return;
            }

            $scope.value = value;
        };

        $scope.enter = function (value) {
            if (!$scope.readonly) {
                $scope.val = value;
            }
            $scope.onHover({value: value});
        };

        $scope.reset = function () {
            $scope.val = angular.copy($scope.value);
            $scope.onLeave();
        };

        $scope.$watch('value', function (value) {
            $scope.val = value;
        });

        $scope.readonly = false;
        if ($attrs.readonly) {
            $scope.$parent.$watch($parse($attrs.readonly), function (value) {
                $scope.readonly = !!value;
            });
        }
    }])

    .directive('rating', function () {
        return {
            restrict: 'EA',
            scope: {
                value: '=',
                onHover: '&',
                onLeave: '&'
            },
            controller: 'RatingController',
            templateUrl: 'template/rating/rating.html',
            replace: true
        };
    });

/**
 * @ngdoc overview
 * @name ui.bootstrap.tabs
 *
 * @description
 * AngularJS version of the tabs directive.
 */

angular.module('ui.bootstrap.tabs', [])

    .directive('tabs', function () {
        return function () {
            throw new Error("The `tabs` directive is deprecated, please migrate to `tabset`. Instructions can be found at http://github.com/angular-ui/bootstrap/tree/master/CHANGELOG.md");
        };
    })

    .controller('TabsetController', ['$scope', '$element',
        function TabsetCtrl($scope, $element) {

            var ctrl = this,
                tabs = ctrl.tabs = $scope.tabs = [];

            ctrl.select = function (tab) {
                angular.forEach(tabs, function (tab) {
                    tab.active = false;
                });
                tab.active = true;
            };

            ctrl.addTab = function addTab(tab) {
                tabs.push(tab);
                if (tabs.length === 1 || tab.active) {
                    ctrl.select(tab);
                }
            };

            ctrl.removeTab = function removeTab(tab) {
                var index = tabs.indexOf(tab);
                //Select a new tab if the tab to be removed is selected
                if (tab.active && tabs.length > 1) {
                    //If this is the last tab, select the previous tab. else, the next tab.
                    var newActiveIndex = index === tabs.length - 1 ? index - 1 : index + 1;
                    ctrl.select(tabs[newActiveIndex]);
                }
                tabs.splice(index, 1);
            };
        }])

/**
 * @ngdoc directive
 * @name ui.bootstrap.tabs.directive:tabset
 * @restrict EA
 *
 * @description
 * Tabset is the outer container for the tabs directive
 *
 * @param {boolean=} vertical Whether or not to use vertical styling for the tabs.
 * @param {string=} direction  What direction the tabs should be rendered. Available:
 * 'right', 'left', 'below'.
 *
 * @example
 <example module="ui.bootstrap">
 <file name="index.html">
 <tabset>
 <tab heading="Vertical Tab 1"><b>First</b> Content!</tab>
 <tab heading="Vertical Tab 2"><i>Second</i> Content!</tab>
 </tabset>
 <hr />
 <tabset vertical="true">
 <tab heading="Vertical Tab 1"><b>First</b> Vertical Content!</tab>
 <tab heading="Vertical Tab 2"><i>Second</i> Vertical Content!</tab>
 </tabset>
 </file>
 </example>
 */
    .directive('tabset', function () {
        return {
            restrict: 'EA',
            transclude: true,
            replace: true,
            require: '^tabset',
            scope: {},
            controller: 'TabsetController',
            templateUrl: 'template/tabs/tabset.html',
            compile: function (elm, attrs, transclude) {
                return {
                    pre: function (scope, element, attrs, tabsetCtrl) {
                        scope.vertical = angular.isDefined(attrs.vertical) ? scope.$parent.$eval(attrs.vertical) : false;
                        scope.type = angular.isDefined(attrs.type) ? scope.$parent.$eval(attrs.type) : 'tabs';
                        scope.direction = angular.isDefined(attrs.direction) ? scope.$parent.$eval(attrs.direction) : 'top';
                        scope.tabsAbove = (scope.direction !== 'below');
                        tabsetCtrl.$scope = scope;
                        tabsetCtrl.$transcludeFn = transclude;
                    }
                };
            }
//      compile: function(elm, attrs, transclude) {
//      return function(scope, element, attrs, tabsetCtrl) {
//        scope.vertical = angular.isDefined(attrs.vertical) ? scope.$parent.$eval(attrs.vertical) : false;
//        scope.type = angular.isDefined(attrs.type) ? scope.$parent.$eval(attrs.type) : 'tabs';
//        scope.direction = angular.isDefined(attrs.direction) ? scope.$parent.$eval(attrs.direction) : 'top';
//        scope.tabsAbove = (scope.direction != 'below');
//        tabsetCtrl.$scope = scope;
//        tabsetCtrl.$transcludeFn = transclude;
//      };
//    }
        };
    })

/**
 * @ngdoc directive
 * @name ui.bootstrap.tabs.directive:tab
 * @restrict EA
 *
 * @param {string=} heading The visible heading, or title, of the tab. Set HTML headings with {@link ui.bootstrap.tabs.directive:tabHeading tabHeading}.
 * @param {string=} select An expression to evaluate when the tab is selected.
 * @param {boolean=} active A binding, telling whether or not this tab is selected.
 * @param {boolean=} disabled A binding, telling whether or not this tab is disabled.
 *
 * @description
 * Creates a tab with a heading and content. Must be placed within a {@link ui.bootstrap.tabs.directive:tabset tabset}.
 *
 * @example
 <example module="ui.bootstrap">
 <file name="index.html">
 <div ng-controller="TabsDemoCtrl">
 <button class="btn btn-small" ng-click="items[0].active = true">
 Select item 1, using active binding
 </button>
 <button class="btn btn-small" ng-click="items[1].disabled = !items[1].disabled">
 Enable/disable item 2, using disabled binding
 </button>
 <br />
 <tabset>
 <tab heading="Tab 1">First Tab</tab>
 <tab select="alertMe()">
 <tab-heading><i class="icon-bell"></i> Alert me!</tab-heading>
 Second Tab, with alert callback and html heading!
 </tab>
 <tab ng-repeat="item in items"
 heading="{{item.title}}"
 disabled="item.disabled"
 active="item.active">
 {{item.content}}
 </tab>
 </tabset>
 </div>
 </file>
 <file name="script.js">
 function TabsDemoCtrl($scope) {
      $scope.items = [
        { title:"Dynamic Title 1", content:"Dynamic Item 0" },
        { title:"Dynamic Title 2", content:"Dynamic Item 1", disabled: true }
      ];

      $scope.alertMe = function() {
        setTimeout(function() {
          alert("You've selected the alert tab!");
        });
      };
    };
 </file>
 </example>
 */

/**
 * @ngdoc directive
 * @name ui.bootstrap.tabs.directive:tabHeading
 * @restrict EA
 *
 * @description
 * Creates an HTML heading for a {@link ui.bootstrap.tabs.directive:tab tab}. Must be placed as a child of a tab element.
 *
 * @example
 <example module="ui.bootstrap">
 <file name="index.html">
 <tabset>
 <tab>
 <tab-heading><b>HTML</b> in my titles?!</tab-heading>
 And some content, too!
 </tab>
 <tab>
 <tab-heading><i class="icon-heart"></i> Icon heading?!?</tab-heading>
 That's right.
 </tab>
 </tabset>
 </file>
 </example>
 */
    .directive('tab', ['$parse', '$http', '$templateCache', '$compile',
        function ($parse, $http, $templateCache, $compile) {
            return {
                require: '^tabset',
                restrict: 'EA',
                replace: true,
                templateUrl: 'template/tabs/tab.html',
                transclude: true,
                scope: {
                    heading: '@',
                    onSelect: '&select', //This callback is called in contentHeadingTransclude
                    //once it inserts the tab's content into the dom
                    onDeselect: '&deselect'
                },
                controller: function () {
                    //Empty controller so other directives can require being 'under' a tab
                },
                compile: function (elm, attrs, transclude) {
                    return function postLink(scope, elm, attrs, tabsetCtrl) {
                        var getActive, setActive;
                        if (attrs.active) {
                            getActive = $parse(attrs.active);
                            setActive = getActive.assign;
                            scope.$parent.$watch(getActive, function updateActive(value) {
                                scope.active = !!value;
                            });
                            scope.active = getActive(scope.$parent);
                        } else {
                            setActive = getActive = angular.noop;
                        }

                        scope.$watch('active', function (active) {
                            setActive(scope.$parent, active);
                            if (active) {
                                tabsetCtrl.select(scope);
                                scope.onSelect();
                            } else {
                                scope.onDeselect();
                            }
                        });

                        scope.disabled = false;
                        if (attrs.disabled) {
                            scope.$parent.$watch($parse(attrs.disabled), function (value) {
                                scope.disabled = !!value;
                            });
                        }

                        scope.select = function () {
                            if (!scope.disabled) {
                                scope.active = true;
                            }
                        };

                        tabsetCtrl.addTab(scope);
                        scope.$on('$destroy', function () {
                            tabsetCtrl.removeTab(scope);
                        });
                        if (scope.active) {
                            setActive(scope.$parent, true);
                        }


                        //We need to transclude later, once the content container is ready.
                        //when this link happens, we're inside a tab heading.
                        scope.$transcludeFn = transclude;
                    };
                }
            };
        }])

    .directive('tabHeadingTransclude', [function () {
        return {
            restrict: 'A',
            require: '^tab',
            link: function (scope, elm, attrs, tabCtrl) {
                scope.$watch('headingElement', function updateHeadingElement(heading) {
                    if (heading) {
                        elm.html('');
                        elm.append(heading);
                    }
                });
            }
        };
    }])

    .directive('tabContentTransclude', ['$compile', '$parse', function ($compile, $parse) {
        function isTabHeading(node) {
            return node.tagName && (
                node.hasAttribute('tab-heading') ||
                    node.hasAttribute('data-tab-heading') ||
                    node.tagName.toLowerCase() === 'tab-heading' ||
                    node.tagName.toLowerCase() === 'data-tab-heading'
                );
        }

        return {
            restrict: 'A',
            require: '^tabset',
            link: function (scope, elm, attrs) {
                var tab = scope.$eval(attrs.tabContentTransclude);

                //Now our tab is ready to be transcluded: both the tab heading area
                //and the tab content area are loaded.  Transclude 'em both.
                tab.$transcludeFn(tab.$parent, function (contents) {
                    angular.forEach(contents, function (node) {
                        if (isTabHeading(node)) {
                            //Let tabHeadingTransclude know.
                            tab.headingElement = node;
                        } else {
                            elm.append(node);
                        }
                    });
                });
            }
        };
    }])

    .directive('tabsetTitles', ['$http', function ($http) {
        return {
            restrict: 'A',
            require: '^tabset',
            templateUrl: 'template/tabs/tabset-titles.html',
            replace: true,
            link: function (scope, elm, attrs, tabsetCtrl) {
                if (!scope.$eval(attrs.tabsetTitles)) {
                    elm.remove();
                } else {
                    //now that tabs location has been decided, transclude the tab titles in
                    tabsetCtrl.$transcludeFn(tabsetCtrl.$scope.$parent, function (node) {
                        elm.append(node);
                    });
                }
            }
        };
    }])

;


angular.module('ui.bootstrap.timepicker', [])

    .constant('timepickerConfig', {
        hourStep: 1,
        minuteStep: 1,
        showMeridian: true,
        meridians: ['AM', 'PM'],
        readonlyInput: false,
        mousewheel: true
    })

    .directive('timepicker', ['$parse', '$log', 'timepickerConfig', function ($parse, $log, timepickerConfig) {
        return {
            restrict: 'EA',
            require: '?^ngModel',
            replace: true,
            scope: {},
            templateUrl: 'template/timepicker/timepicker.html',
            link: function (scope, element, attrs, ngModel) {
                if (!ngModel) {
                    return; // do nothing if no ng-model
                }

                var selected = new Date(), meridians = timepickerConfig.meridians;

                var hourStep = timepickerConfig.hourStep;
                if (attrs.hourStep) {
                    scope.$parent.$watch($parse(attrs.hourStep), function (value) {
                        hourStep = parseInt(value, 10);
                    });
                }

                var minuteStep = timepickerConfig.minuteStep;
                if (attrs.minuteStep) {
                    scope.$parent.$watch($parse(attrs.minuteStep), function (value) {
                        minuteStep = parseInt(value, 10);
                    });
                }

                // 12H / 24H mode
                scope.showMeridian = timepickerConfig.showMeridian;
                if (attrs.showMeridian) {
                    scope.$parent.$watch($parse(attrs.showMeridian), function (value) {
                        scope.showMeridian = !!value;

                        if (ngModel.$error.time) {
                            // Evaluate from template
                            var hours = getHoursFromTemplate(), minutes = getMinutesFromTemplate();
                            if (angular.isDefined(hours) && angular.isDefined(minutes)) {
                                selected.setHours(hours);
                                refresh();
                            }
                        } else {
                            updateTemplate();
                        }
                    });
                }

                // Get scope.hours in 24H mode if valid
                function getHoursFromTemplate() {
                    var hours = parseInt(scope.hours, 10);
                    var valid = ( scope.showMeridian ) ? (hours > 0 && hours < 13) : (hours >= 0 && hours < 24);
                    if (!valid) {
                        return undefined;
                    }

                    if (scope.showMeridian) {
                        if (hours === 12) {
                            hours = 0;
                        }
                        if (scope.meridian === meridians[1]) {
                            hours = hours + 12;
                        }
                    }
                    return hours;
                }

                function getMinutesFromTemplate() {
                    var minutes = parseInt(scope.minutes, 10);
                    return ( minutes >= 0 && minutes < 60 ) ? minutes : undefined;
                }

                function pad(value) {
                    return ( angular.isDefined(value) && value.toString().length < 2 ) ? '0' + value : value;
                }

                // Input elements
                var inputs = element.find('input'), hoursInputEl = inputs.eq(0), minutesInputEl = inputs.eq(1);

                // Respond on mousewheel spin
                var mousewheel = (angular.isDefined(attrs.mousewheel)) ? scope.$eval(attrs.mousewheel) : timepickerConfig.mousewheel;
                if (mousewheel) {

                    var isScrollingUp = function (e) {
                        if (e.originalEvent) {
                            e = e.originalEvent;
                        }
                        //pick correct delta variable depending on event
                        var delta = (e.wheelDelta) ? e.wheelDelta : -e.deltaY;
                        return (e.detail || delta > 0);
                    };

                    hoursInputEl.bind('mousewheel wheel', function (e) {
                        scope.$apply((isScrollingUp(e)) ? scope.incrementHours() : scope.decrementHours());
                        e.preventDefault();
                    });

                    minutesInputEl.bind('mousewheel wheel', function (e) {
                        scope.$apply((isScrollingUp(e)) ? scope.incrementMinutes() : scope.decrementMinutes());
                        e.preventDefault();
                    });
                }

                scope.readonlyInput = (angular.isDefined(attrs.readonlyInput)) ? scope.$eval(attrs.readonlyInput) : timepickerConfig.readonlyInput;
                if (!scope.readonlyInput) {

                    var invalidate = function (invalidHours, invalidMinutes) {
                        ngModel.$setViewValue(null);
                        ngModel.$setValidity('time', false);
                        if (angular.isDefined(invalidHours)) {
                            scope.invalidHours = invalidHours;
                        }
                        if (angular.isDefined(invalidMinutes)) {
                            scope.invalidMinutes = invalidMinutes;
                        }
                    };

                    scope.updateHours = function () {
                        var hours = getHoursFromTemplate();

                        if (angular.isDefined(hours)) {
                            selected.setHours(hours);
                            refresh('h');
                        } else {
                            invalidate(true);
                        }
                    };

                    hoursInputEl.bind('blur', function (e) {
                        if (!scope.validHours && scope.hours < 10) {
                            scope.$apply(function () {
                                scope.hours = pad(scope.hours);
                            });
                        }
                    });

                    scope.updateMinutes = function () {
                        var minutes = getMinutesFromTemplate();

                        if (angular.isDefined(minutes)) {
                            selected.setMinutes(minutes);
                            refresh('m');
                        } else {
                            invalidate(undefined, true);
                        }
                    };

                    minutesInputEl.bind('blur', function (e) {
                        if (!scope.invalidMinutes && scope.minutes < 10) {
                            scope.$apply(function () {
                                scope.minutes = pad(scope.minutes);
                            });
                        }
                    });
                } else {
                    scope.updateHours = angular.noop;
                    scope.updateMinutes = angular.noop;
                }

                ngModel.$render = function () {
                    var date = ngModel.$modelValue ? new Date(ngModel.$modelValue) : null;

                    if (isNaN(date)) {
                        ngModel.$setValidity('time', false);
                        $log.error('Timepicker directive: "ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.');
                    } else {
                        if (date) {
                            selected = date;
                        }
                        makeValid();
                        updateTemplate();
                    }
                };

                // Call internally when we know that model is valid.
                function refresh(keyboardChange) {
                    makeValid();
                    ngModel.$setViewValue(new Date(selected));
                    updateTemplate(keyboardChange);
                }

                function makeValid() {
                    ngModel.$setValidity('time', true);
                    scope.invalidHours = false;
                    scope.invalidMinutes = false;
                }

                function updateTemplate(keyboardChange) {
                    var hours = selected.getHours(), minutes = selected.getMinutes();

                    if (scope.showMeridian) {
                        hours = ( hours === 0 || hours === 12 ) ? 12 : hours % 12; // Convert 24 to 12 hour system
                    }
                    scope.hours = keyboardChange === 'h' ? hours : pad(hours);
                    scope.minutes = keyboardChange === 'm' ? minutes : pad(minutes);
                    scope.meridian = selected.getHours() < 12 ? meridians[0] : meridians[1];
                }

                function addMinutes(minutes) {
                    var dt = new Date(selected.getTime() + minutes * 60000);
                    selected.setHours(dt.getHours(), dt.getMinutes());
                    refresh();
                }

                scope.incrementHours = function () {
                    addMinutes(hourStep * 60);
                };
                scope.decrementHours = function () {
                    addMinutes(-hourStep * 60);
                };
                scope.incrementMinutes = function () {
                    addMinutes(minuteStep);
                };
                scope.decrementMinutes = function () {
                    addMinutes(-minuteStep);
                };
                scope.toggleMeridian = function () {
                    addMinutes(12 * 60 * (( selected.getHours() < 12 ) ? 1 : -1));
                };
            }
        };
    }]);

angular.module('ui.bootstrap.typeahead', ['ui.bootstrap.position', 'ui.bootstrap.bindHtml'])

/**
 * A helper service that can parse typeahead's syntax (string provided by users)
 * Extracted to a separate service for ease of unit testing
 */
    .factory('typeaheadParser', ['$parse', function ($parse) {

        //                      00000111000000000000022200000000000000003333333333333330000000000044000
        var TYPEAHEAD_REGEXP = /^\s*(.*?)(?:\s+as\s+(.*?))?\s+for\s+(?:([\$\w][\$\w\d]*))\s+in\s+(.*)$/;

        return {
            parse: function (input) {

                var match = input.match(TYPEAHEAD_REGEXP), modelMapper, viewMapper, source;
                if (!match) {
                    throw new Error(
                        "Expected typeahead specification in form of '_modelValue_ (as _label_)? for _item_ in _collection_'" +
                            " but got '" + input + "'.");
                }

                return {
                    itemName: match[3],
                    source: $parse(match[4]),
                    viewMapper: $parse(match[2] || match[1]),
                    modelMapper: $parse(match[1])
                };
            }
        };
    }])

    .directive('typeahead', ['$compile', '$parse', '$q', '$timeout', '$document', '$position', 'typeaheadParser',
        function ($compile, $parse, $q, $timeout, $document, $position, typeaheadParser) {

            var HOT_KEYS = [9, 13, 27, 38, 40];

            return {
                require: 'ngModel',
                link: function (originalScope, element, attrs, modelCtrl) {

                    //SUPPORTED ATTRIBUTES (OPTIONS)

                    //minimal no of characters that needs to be entered before typeahead kicks-in
                    var minSearch = originalScope.$eval(attrs.typeaheadMinLength) || 1;

                    //minimal wait time after last character typed before typehead kicks-in
                    var waitTime = originalScope.$eval(attrs.typeaheadWaitMs) || 0;

                    //should it restrict model values to the ones selected from the popup only?
                    var isEditable = originalScope.$eval(attrs.typeaheadEditable) !== false;

                    //binding to a variable that indicates if matches are being retrieved asynchronously
                    var isLoadingSetter = $parse(attrs.typeaheadLoading).assign || angular.noop;

                    //a callback executed when a match is selected
                    var onSelectCallback = $parse(attrs.typeaheadOnSelect);

                    var inputFormatter = attrs.typeaheadInputFormatter ? $parse(attrs.typeaheadInputFormatter) : undefined;

                    //INTERNAL VARIABLES

                    //model setter executed upon match selection
                    var $setModelValue = $parse(attrs.ngModel).assign;

                    //expressions used by typeahead
                    var parserResult = typeaheadParser.parse(attrs.typeahead);


                    //pop-up element used to display matches
                    var popUpEl = angular.element('<typeahead-popup></typeahead-popup>');
                    popUpEl.attr({
                        matches: 'matches',
                        active: 'activeIdx',
                        select: 'select(activeIdx)',
                        query: 'query',
                        position: 'position'
                    });
                    //custom item template
                    if (angular.isDefined(attrs.typeaheadTemplateUrl)) {
                        popUpEl.attr('template-url', attrs.typeaheadTemplateUrl);
                    }

                    //create a child scope for the typeahead directive so we are not polluting original scope
                    //with typeahead-specific data (matches, query etc.)
                    var scope = originalScope.$new();
                    originalScope.$on('$destroy', function () {
                        scope.$destroy();
                    });

                    var resetMatches = function () {
                        scope.matches = [];
                        scope.activeIdx = -1;
                    };

                    var getMatchesAsync = function (inputValue) {

                        var locals = {$viewValue: inputValue};
                        isLoadingSetter(originalScope, true);
                        $q.when(parserResult.source(scope, locals)).then(function (matches) {

                            //it might happen that several async queries were in progress if a user were typing fast
                            //but we are interested only in responses that correspond to the current view value
                            if (inputValue === modelCtrl.$viewValue) {
                                if (matches.length > 0) {

                                    scope.activeIdx = 0;
                                    scope.matches.length = 0;

                                    //transform labels
                                    for (var i = 0; i < matches.length; i++) {
                                        locals[parserResult.itemName] = matches[i];
                                        scope.matches.push({
                                            label: parserResult.viewMapper(scope, locals),
                                            model: matches[i]
                                        });
                                    }

                                    scope.query = inputValue;
                                    //position pop-up with matches - we need to re-calculate its position each time we are opening a window
                                    //with matches as a pop-up might be absolute-positioned and position of an input might have changed on a page
                                    //due to other elements being rendered
                                    scope.position = $position.position(element);
                                    scope.position.top = scope.position.top + element.prop('offsetHeight');

                                } else {
                                    resetMatches();
                                }
                                isLoadingSetter(originalScope, false);
                            }
                        }, function () {
                            resetMatches();
                            isLoadingSetter(originalScope, false);
                        });
                    };

                    resetMatches();

                    //we need to propagate user's query so we can higlight matches
                    scope.query = undefined;

                    //Declare the timeout promise var outside the function scope so that stacked calls can be cancelled later
                    var timeoutPromise;

                    //plug into $parsers pipeline to open a typeahead on view changes initiated from DOM
                    //$parsers kick-in on all the changes coming from the view as well as manually triggered by $setViewValue
                    modelCtrl.$parsers.unshift(function (inputValue) {

                        resetMatches();
                        if (inputValue && inputValue.length >= minSearch) {
                            if (waitTime > 0) {
                                if (timeoutPromise) {
                                    $timeout.cancel(timeoutPromise);//cancel previous timeout
                                }
                                timeoutPromise = $timeout(function () {
                                    getMatchesAsync(inputValue);
                                }, waitTime);
                            } else {
                                getMatchesAsync(inputValue);
                            }
                        }

                        if (isEditable) {
                            return inputValue;
                        } else {
                            modelCtrl.$setValidity('editable', false);
                            return undefined;
                        }
                    });

                    modelCtrl.$formatters.push(function (modelValue) {

                        var candidateViewValue, emptyViewValue;
                        var locals = {};

                        if (inputFormatter) {

                            locals['$model'] = modelValue;
                            return inputFormatter(originalScope, locals);

                        } else {

                            //it might happen that we don't have enough info to properly render input value
                            //we need to check for this situation and simply return model value if we can't apply custom formatting
                            locals[parserResult.itemName] = modelValue;
                            candidateViewValue = parserResult.viewMapper(originalScope, locals);
                            locals[parserResult.itemName] = undefined;
                            emptyViewValue = parserResult.viewMapper(originalScope, locals);

                            return candidateViewValue !== emptyViewValue ? candidateViewValue : modelValue;
                        }
                    });

                    scope.select = function (activeIdx) {
                        //called from within the $digest() cycle
                        var locals = {};
                        var model, item;

                        locals[parserResult.itemName] = item = scope.matches[activeIdx].model;
                        model = parserResult.modelMapper(originalScope, locals);
                        $setModelValue(originalScope, model);
                        modelCtrl.$setValidity('editable', true);

                        onSelectCallback(originalScope, {
                            $item: item,
                            $model: model,
                            $label: parserResult.viewMapper(originalScope, locals)
                        });

                        resetMatches();

                        //return focus to the input element if a mach was selected via a mouse click event
                        element[0].focus();
                    };

                    //bind keyboard events: arrows up(38) / down(40), enter(13) and tab(9), esc(27)
                    element.bind('keydown', function (evt) {

                        //typeahead is open and an "interesting" key was pressed
                        if (scope.matches.length === 0 || HOT_KEYS.indexOf(evt.which) === -1) {
                            return;
                        }

                        evt.preventDefault();

                        if (evt.which === 40) {
                            scope.activeIdx = (scope.activeIdx + 1) % scope.matches.length;
                            scope.$digest();

                        } else if (evt.which === 38) {
                            scope.activeIdx = (scope.activeIdx ? scope.activeIdx : scope.matches.length) - 1;
                            scope.$digest();

                        } else if (evt.which === 13 || evt.which === 9) {
                            scope.$apply(function () {
                                scope.select(scope.activeIdx);
                            });

                        } else if (evt.which === 27) {
                            evt.stopPropagation();

                            resetMatches();
                            scope.$digest();
                        }
                    });

                    // Keep reference to click handler to unbind it.
                    var dismissClickHandler = function (evt) {
                        if (element[0] !== evt.target) {
                            resetMatches();
                            scope.$digest();
                        }
                    };

                    $document.bind('click', dismissClickHandler);

                    originalScope.$on('$destroy', function () {
                        $document.unbind('click', dismissClickHandler);
                    });

                    element.after($compile(popUpEl)(scope));
                }
            };

        }])

    .directive('typeaheadPopup', function () {
        return {
            restrict: 'E',
            scope: {
                matches: '=',
                query: '=',
                active: '=',
                position: '=',
                select: '&'
            },
            replace: true,
            templateUrl: 'template/typeahead/typeahead-popup.html',
            link: function (scope, element, attrs) {

                scope.templateUrl = attrs.templateUrl;

                scope.isOpen = function () {
                    return scope.matches.length > 0;
                };

                scope.isActive = function (matchIdx) {
                    return scope.active === matchIdx;
                };

                scope.selectActive = function (matchIdx) {
                    scope.active = matchIdx;
                };

                scope.selectMatch = function (activeIdx) {
                    scope.select({activeIdx: activeIdx});
                };
            }
        };
    })

    .directive('typeaheadMatch', ['$http', '$templateCache', '$compile', '$parse', function ($http, $templateCache, $compile, $parse) {
        return {
            restrict: 'E',
            scope: {
                index: '=',
                match: '=',
                query: '='
            },
            link: function (scope, element, attrs) {
                var tplUrl = $parse(attrs.templateUrl)(scope.$parent) || 'template/typeahead/typeahead-match.html';
                $http.get(tplUrl, {cache: $templateCache}).success(function (tplContent) {
                    element.replaceWith($compile(tplContent.trim())(scope));
                });
            }
        };
    }])

    .filter('typeaheadHighlight', function () {

        function escapeRegexp(queryToEscape) {
            return queryToEscape.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
        }

        return function (matchItem, query) {
            return query ? matchItem.replace(new RegExp(escapeRegexp(query), 'gi'), '<strong>$&</strong>') : matchItem;
        };
    });
angular.module("template/accordion/accordion-group.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/accordion/accordion-group.html",
        "<div class=\"accordion-group\">\n" +
            "  <div class=\"accordion-heading\" ><a class=\"accordion-toggle\" ng-click=\"isOpen = !isOpen\" accordion-transclude=\"heading\">{{heading}}</a></div>\n" +
            "  <div class=\"accordion-body\" collapse=\"!isOpen\">\n" +
            "    <div class=\"accordion-inner\" ng-transclude></div>  </div>\n" +
            "</div>");
}]);

angular.module("template/accordion/accordion.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/accordion/accordion.html",
        "<div class=\"accordion\" ng-transclude></div>");
}]);

angular.module("template/alert/alert.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/alert/alert.html",
        "<div class='alert' ng-class='type && \"alert-\" + type'>\n" +
            "    <button ng-show='closeable' type='button' class='close' ng-click='close()'>&times;</button>\n" +
            "    <div ng-transclude></div>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/modal/backdrop.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/modal/backdrop.html",
        "<div class=\"modal-backdrop fade\" ng-class=\"{in: animate}\" ng-style=\"{'z-index': 1040 + index*10}\" ng-click=\"close($event)\"></div>");
}]);

angular.module("template/modal/window.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/modal/window.html",
        "<div class=\"modal fade {{ windowClass }}\" ng-class=\"{in: animate}\" ng-style=\"{'z-index': 1050 + index*10}\" ng-transclude></div>");
}]);

angular.module("template/pagination/pager.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/pagination/pager.html",
        "<div class=\"pager\">\n" +
            "  <ul>\n" +
            "    <li ng-repeat=\"page in pages\" ng-class=\"{disabled: page.disabled, previous: page.previous, next: page.next}\"><a ng-click=\"selectPage(page.number)\">{{page.text}}</a></li>\n" +
            "  </ul>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/pagination/pagination.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/pagination/pagination.html",
        "<div class=\"pagination\"><ul>\n" +
            "  <li ng-repeat=\"page in pages\" ng-class=\"{active: page.active, disabled: page.disabled}\"><a ng-click=\"selectPage(page.number)\">{{page.text}}</a></li>\n" +
            "  </ul>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/tooltip/tooltip-html-unsafe-popup.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tooltip/tooltip-html-unsafe-popup.html",
        "<div class=\"tooltip {{placement}}\" ng-class=\"{ in: isOpen(), fade: animation() }\">\n" +
            "  <div class=\"tooltip-arrow\"></div>\n" +
            "  <div class=\"tooltip-inner\" ng-bind-html-unsafe=\"content\"></div>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/tooltip/tooltip-popup.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tooltip/tooltip-popup.html",
        "<div class=\"tooltip {{placement}}\" ng-class=\"{ in: isOpen(), fade: animation() }\">\n" +
            "  <div class=\"tooltip-arrow\"></div>\n" +
            "  <div class=\"tooltip-inner\" ng-bind=\"content\"></div>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/popover/popover.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/popover/popover.html",
        "<div class=\"popover {{placement}}\" ng-class=\"{ in: isOpen(), fade: animation() }\">\n" +
            "  <div class=\"arrow\"></div>\n" +
            "\n" +
            "  <div class=\"popover-inner\">\n" +
            "      <h3 class=\"popover-title\" ng-bind=\"title\" ng-show=\"title\"></h3>\n" +
            "      <div class=\"popover-content\" ng-bind=\"content\"></div>\n" +
            "  </div>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/progressbar/bar.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/progressbar/bar.html",
        "<div class=\"bar\" ng-class='type && \"bar-\" + type'></div>");
}]);

angular.module("template/progressbar/progress.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/progressbar/progress.html",
        "<div class=\"progress\"><progressbar ng-repeat=\"bar in bars\" width=\"bar.to\" old=\"bar.from\" animate=\"bar.animate\" type=\"bar.type\"></progressbar></div>");
}]);

angular.module("template/rating/rating.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/rating/rating.html",
        "<span ng-mouseleave=\"reset()\">\n" +
            "	<i ng-repeat=\"r in range\" ng-mouseenter=\"enter($index + 1)\" ng-click=\"rate($index + 1)\" ng-class=\"$index < val && (r.stateOn || 'icon-star') || (r.stateOff || 'icon-star-empty')\"></i>\n" +
            "</span>");
}]);

angular.module("template/tabs/pane.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tabs/pane.html",
        "<div class=\"tab-pane\" ng-class=\"{active: selected}\" ng-show=\"selected\" ng-transclude></div>\n" +
            "");
}]);

angular.module("template/tabs/tab.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tabs/tab.html",
        "<li ng-class=\"{active: active, disabled: disabled}\">\n" +
            "  <a ng-click=\"select()\" tab-heading-transclude>{{heading}}</a>\n" +
            "</li>\n" +
            "");
}]);

angular.module("template/tabs/tabs.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tabs/tabs.html",
        "<div class=\"tabbable\">\n" +
            "  <ul class=\"nav nav-tabs\">\n" +
            "    <li ng-repeat=\"pane in panes\" ng-class=\"{active:pane.selected}\">\n" +
            "      <a ng-click=\"select(pane)\">{{pane.heading}}</a>\n" +
            "    </li>\n" +
            "  </ul>\n" +
            "  <div class=\"tab-content\" ng-transclude></div>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/tabs/tabset-titles.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tabs/tabset-titles.html",
        "<ul class=\"nav {{type && 'nav-' + type}}\" ng-class=\"{'nav-stacked': vertical}\">\n" +
            "</ul>\n" +
            "");
}]);

angular.module("template/tabs/tabset.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/tabs/tabset.html",
        "\n" +
            "<div class=\"tabbable\" ng-class=\"{'tabs-right': direction == 'right', 'tabs-left': direction == 'left', 'tabs-below': direction == 'below'}\">\n" +
            "  <div tabset-titles=\"tabsAbove\"></div>\n" +
            "  <div class=\"tab-content\">\n" +
            "    <div class=\"tab-pane\" \n" +
            "         ng-repeat=\"tab in tabs\" \n" +
            "         ng-class=\"{active: tab.active}\"\n" +
            "         tab-content-transclude=\"tab\">\n" +
            "    </div>\n" +
            "  </div>\n" +
            "  <div tabset-titles=\"!tabsAbove\"></div>\n" +
            "</div>\n" +
            "");
}]);

angular.module("template/timepicker/timepicker.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/timepicker/timepicker.html",
        "<table class=\"form-inline\">\n" +
            "	<tr class=\"text-center\">\n" +
            "		<td><a ng-click=\"incrementHours()\" class=\"btn btn-link\"><i class=\"icon-chevron-up\"></i></a></td>\n" +
            "		<td>&nbsp;</td>\n" +
            "		<td><a ng-click=\"incrementMinutes()\" class=\"btn btn-link\"><i class=\"icon-chevron-up\"></i></a></td>\n" +
            "		<td ng-show=\"showMeridian\"></td>\n" +
            "	</tr>\n" +
            "	<tr>\n" +
            "		<td class=\"control-group\" ng-class=\"{'error': invalidHours}\"><input type=\"text\" ng-model=\"hours\" ng-change=\"updateHours()\" class=\"span1 text-center\" ng-mousewheel=\"incrementHours()\" ng-readonly=\"readonlyInput\" maxlength=\"2\" /></td>\n" +
            "		<td>:</td>\n" +
            "		<td class=\"control-group\" ng-class=\"{'error': invalidMinutes}\"><input type=\"text\" ng-model=\"minutes\" ng-change=\"updateMinutes()\" class=\"span1 text-center\" ng-readonly=\"readonlyInput\" maxlength=\"2\"></td>\n" +
            "		<td ng-show=\"showMeridian\"><button type=\"button\" ng-click=\"toggleMeridian()\" class=\"btn text-center\">{{meridian}}</button></td>\n" +
            "	</tr>\n" +
            "	<tr class=\"text-center\">\n" +
            "		<td><a ng-click=\"decrementHours()\" class=\"btn btn-link\"><i class=\"icon-chevron-down\"></i></a></td>\n" +
            "		<td>&nbsp;</td>\n" +
            "		<td><a ng-click=\"decrementMinutes()\" class=\"btn btn-link\"><i class=\"icon-chevron-down\"></i></a></td>\n" +
            "		<td ng-show=\"showMeridian\"></td>\n" +
            "	</tr>\n" +
            "</table>");
}]);

angular.module("template/typeahead/typeahead-match.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/typeahead/typeahead-match.html",
        "<a tabindex=\"-1\" bind-html-unsafe=\"match.label | typeaheadHighlight:query\"></a>");
}]);

angular.module("template/typeahead/typeahead-popup.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/typeahead/typeahead-popup.html",
        "<ul class=\"typeahead dropdown-menu\" ng-style=\"{display: isOpen()&&'block' || 'none', top: position.top+'px', left: position.left+'px'}\">\n" +
            "    <li ng-repeat=\"match in matches\" ng-class=\"{active: isActive($index) }\" ng-mouseenter=\"selectActive($index)\" ng-click=\"selectMatch($index)\">\n" +
            "        <typeahead-match index=\"$index\" match=\"match\" query=\"query\" template-url=\"templateUrl\"></typeahead-match>\n" +
            "    </li>\n" +
            "</ul>");
}]);

angular.module("template/typeahead/typeahead.html", []).run(["$templateCache", function ($templateCache) {
    $templateCache.put("template/typeahead/typeahead.html",
        "<ul class=\"typeahead dropdown-menu\" ng-style=\"{display: isOpen()&&'block' || 'none', top: position.top+'px', left: position.left+'px'}\">\n" +
            "    <li ng-repeat=\"match in matches\" ng-class=\"{active: isActive($index) }\" ng-mouseenter=\"selectActive($index)\">\n" +
            "        <a tabindex=\"-1\" ng-click=\"selectMatch($index)\" ng-bind-html-unsafe=\"match.label | typeaheadHighlight:query\"></a>\n" +
            "    </li>\n" +
            "</ul>");
}]);
