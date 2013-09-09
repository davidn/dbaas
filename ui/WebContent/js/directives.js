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
    }]);


