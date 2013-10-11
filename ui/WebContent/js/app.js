angular.module('GenieDBaaS', ['GenieDBaaS.config', 'Utility.directives', 'GenieDBaaS.services', 'ui.directives', 'ui.bootstrap.tooltipX', 'ngRoute', 'ngSanitize', 'ngResource', 'ngStorage', 'ui.select2', 'ui.bootstrap', 'angulartics', 'angulartics.google.analytics', "messageBox"])
    .config(function ($routeProvider, $httpProvider) {
        $routeProvider.
            when("/", {templateUrl: 'part/welcome.html', controller: WelcomeCntl}).
            when("/forgot", {templateUrl: 'part/forgot.html', controller: ForgotCntl}).
            when("/list", {templateUrl: 'part/list.html', controller: ListCntl}).
            when("/try", {templateUrl: 'part/try.html', controller: RegisterCntl}).
            when("/thankyou", {templateUrl: 'part/thanks.html', controller: ThanksCntl}).
            when("/activate/:activationHash", {templateUrl: 'part/activate.html', controller: ActivationCntl}).
            when("/quickstart", {templateUrl: 'part/quickstart.html', controller: QuickStartCntl}).
            when("/cluster", {templateUrl: 'part/cluster.html', controller: ClusterCntl}).
            when("/cluster/:clusterid/node", {templateUrl: 'part/node.html', controller: NodeCntl}).
            when("/monitor", {templateUrl: 'part/monitor.html', controller: QuickStartCntl}).
            when("/logout", {templateUrl: 'part/welcome.html', controller: LogoutCntl}).
            when("/impersonate/:token", {templateUrl: 'part/impersonate.html', controller: ImpersonateCntl}).
            otherwise({redirectTo: '/'});

        var interceptor = function ($location, $q, growl) {
            function success(response) {
                return response;
            };

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
            }
        };

        $httpProvider.responseInterceptors.push(interceptor);

        $.fn.sparkline.defaults.common.lineColor = '#8e8e8e';
        $.fn.sparkline.defaults.common.fillColor = undefined;
    })
    .config([
        '$compileProvider',
        function ($compileProvider) {
            $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|blob|data):/);
        }
    ]);

