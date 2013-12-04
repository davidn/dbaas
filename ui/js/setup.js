angular.module('geniedb', ['ui.keypress', 'ui.bootstrap.tooltipX', 'ngRoute', 'ngSanitize', 'ngResource', 'ngStorage', 'ui.select2', 'ui.bootstrap', 'angulartics', 'angulartics.google.analytics', 'messageBox'])

    .config(function ($routeProvider, $httpProvider, $compileProvider) {

        $routeProvider.
            when('/', {templateUrl: 'partial/welcome/welcome.html'}).
            when('/activate/:activationHash', {templateUrl: 'partial/activate/activate.html'}).
            when('/reset/:activationHash', {templateUrl: 'partial/activate/activate.html', action: 'reset'}).
            when('/cluster', {templateUrl: 'partial/cluster/cluster.html'}).
            when('/cluster/:clusterid/node', {templateUrl: 'partial/node/node.html'}).
            when('/forgot', {templateUrl: 'partial/forgot/forgot.html'}).
            when('/impersonate/:token', {templateUrl: 'partial/impersonate/impersonate.html'}).
            when('/list', {templateUrl: 'partial/list/list.html'}).
            when('/logout', {templateUrl: 'partial/welcome/welcome.html', controller: 'LogoutCtrl'}).
            when('/monitor', {templateUrl: 'partial/monitor/monitor.html'}).
            when('/quickstart', {templateUrl: 'partial/quickstart/quickstart.html'}).
            when('/thankyou', {templateUrl: 'partial/thanks/thanks.html'}).
            when('/try', {templateUrl: 'partial/try/try.html'}).
            when('/share/:promo', {templateUrl: 'partial/share/share.html'}).
            when('/share', {templateUrl: 'partial/share/share.html'}).
            when('/resize/:clusterId/:nodeId', {templateUrl: 'partial/resize/resize.html'}).
            when('/profile', {templateUrl: 'partial/profile/profile.html'}).
            when('/pricing', {templateUrl: 'partial/pricing/pricing.html'}).
            when('/billinginfo', {templateUrl: 'partial/billinginfo/billinginfo.html'}).
            /* Add New Routes Above */
            otherwise({redirectTo: '/'});


        // Clear token and redirect to login if we get a security token error
        var interceptor = function ($location, $q, growl) {
            function success(response) {
                return response;
            }

            function error(response) {
                if (response.status === 401) {
                    if ($location.$$path !== '/') {
                        $location.path("/logout");
                        growl.error({body: 'Session Expired'});
                    }
                }
                return $q.reject(response);
            }

            return function (promise) {
                return promise.then(success, error);
            };
        };

        $httpProvider.responseInterceptors.push(interceptor);


        // Allow blob downloads for the SSL certs
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|blob|data):/);


    })

    .run(function ($rootScope) {

        $rootScope.safeApply = function (fn) {
            var phase = $rootScope.$$phase;
            if (phase === '$apply' || phase === '$digest') {
                if (fn && (typeof(fn) === 'function')) {
                    fn();
                }
            } else {
                this.$apply(fn);
            }
        };


        $.fn.sparkline.defaults.common.lineColor = '#8e8e8e';
        $.fn.sparkline.defaults.common.fillColor = undefined;

    });
