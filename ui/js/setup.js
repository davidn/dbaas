angular.module('geniedb', ['ui.bootstrap','ui']);

angular.module('geniedb').config(function($routeProvider) {

    $routeProvider.
    when('/activate/:activationHash',{templateUrl: 'partial/activate/activate.html'}).
	when('/forgot',{templateUrl: 'partial/forgot/forgot.html'}).
	when('/list',{templateUrl: 'partial/list/list.html'}).
	when('/try',{templateUrl: 'partial/try/try.html'}).
	when('/thankyou',{templateUrl: 'partial/thanks/thanks.html'}).
	when('/quickstart',{templateUrl: 'partial/quickstart/quickstart.html'}).
	when('/cluster',{templateUrl: 'partial/cluster/cluster.html'}).
	when('/cluster/:clusterid/node',{templateUrl: 'partial/node/node.html'}).
	when('/monitor',{templateUrl: 'partial/monitor/monitor.html'}).
	when('/logout',{templateUrl: 'partial/logout/logout.html'}).
	when('/impersonate/:token',{templateUrl: 'partial/impersonate/impersonate.html'}).
	/* Add New Routes Above */
    otherwise({redirectTo:'/home'});
//    when("/logout", {templateUrl: 'part/welcome.html', controller: LogoutCntl}).

});

angular.module('geniedb').run(function($rootScope) {

	$rootScope.safeApply = function(fn) {
		var phase = $rootScope.$$phase;
		if (phase === '$apply' || phase === '$digest') {
			if (fn && (typeof(fn) === 'function')) {
				fn();
			}
		} else {
			this.$apply(fn);
		}
	};

});
