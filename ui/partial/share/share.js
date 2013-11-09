angular.module('geniedb').controller('ShareCtrl', function ($scope, $location, $routeParams, growl) {
    $scope.showDrawing = $routeParams.promo && ($routeParams.promo.toLowerCase() === 'reinvent');
//    growl.success({body: "Account activated!"});

    $scope.done = function () {
        $location.path("/quickstart");
    };

    // Taken from the Twitter Embed code
    !function (d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0], p = /^http:/.test(d.location) ? 'http' : 'https';
        if (!d.getElementById(id)) {
            js = d.createElement(s);
            js.id = id;
            js.src = p + '://platform.twitter.com/widgets.js';
            fjs.parentNode.insertBefore(js, fjs);
        }
    }(document, 'script', 'twitter-wjs');


    // Re-render buttons
    if (typeof twttr !== 'undefined') {
        twttr.widgets.load();
    }

});