angular.module("messageBox", []).run(["$templateCache", function ($templateCache) {
        $templateCache.put("templates/messageBox/messageBox.html",
            "<div class=\"modal-dialog login\"><div class=\"modal-content login\"><form class=\"form-login\"><div class=\"modal-header login\">\n" +
                "	<h3>{{ title }}</h3>\n" +
                "</div>\n" +
                "<div class=\"modal-body\" ng-bind-html=\"message\">\n" +
                "</div>\n" +
                "<div class=\"modal-footer\">\n" +
                "	<button ng-repeat=\"btn in buttons\" ng-click=\"close(btn.result)\" class=\"btn\" ng-class=\"btn.cssClass\">{{ btn.label }}</button>\n" +
                "</div></div></form></div>\n" +
                "");
    }])
    .controller('MessageBoxController', ['$scope', '$modalInstance', 'model', function ($scope, $modalInstance, model) {
        $scope.title = model.title;
        $scope.message = model.message;
        $scope.buttons = model.buttons;
        $scope.close = function (res) {
            $modalInstance.close(res);
        };
    }])
    .factory('messageBox', ['$modal', function ($modal) {
        return {
            open: function (title, message, buttons, modalOptions) {
                var options = {
                    templateUrl: 'templates/messageBox/messageBox.html',
                    controller: 'MessageBoxController',
                    resolve: {
                        model: function () {
                            return {
                                title: title,
                                message: message,
                                buttons: buttons
                            };
                        }
                    }
                }
                if (modalOptions)
                    angular.extend(options, modalOptions);

                return $modal.open(options);
            }
        }
    }]);