angular.module('geniedb').factory("growl", function ($rootScope) {
    // TODO: Clear messages on route success?
    $rootScope.$on('$routeChangeSuccess', function () {
    });
    return {
        success: function (message) {
            toastr.success(message.body, message.title, message);
        },
        info: function (message) {
            toastr.info(message.body, message.title, message);
        },
        warning: function (message) {
            toastr.warning(message.body, message.title, message);
        },
        error: function (message) {
            toastr.error(message.body, message.title, message);
        }
    };
});