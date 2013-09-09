angular.module('GenieDBaaS', ['GenieDBaaS.config','Utility.directives','GenieDBaaS.services', 'ngRoute', 'ngSanitize', 'ngResource', 'ngStorage', 'ui.select2', 'angulartics', 'angulartics.google.analytics']).config(function ($routeProvider) {
    $routeProvider.
        when("/", {templateUrl: 'part/welcome.html', controller: WelcomeCntl}).
        when("/list", {templateUrl: 'part/list.html', controller: ListCntl}).
        when("/try", {templateUrl: 'part/try.html', controller: RegisterCntl}).
        when("/thankyou", {templateUrl: 'part/thanks.html', controller: ThanksCntl}).
        when("/activate/:activationHash", {templateUrl: 'part/activate.html', controller: ActivationCntl}).
        when("/quickstart", {templateUrl: 'part/quickstart.html', controller: QuickStartCntl}).
        when("/cluster", {templateUrl: 'part/cluster.html', controller: ClusterCntl}).
        when("/cluster/:clusterid/node", {templateUrl: 'part/node.html', controller: NodeCntl}).
        when("/monitor", {templateUrl: 'part/monitor.html', controller: QuickStartCntl}).
        otherwise({redirectTo: '/'});
});
