// TODO: Refactor to split IAM from actions
angular.module('geniedb').factory('User', function ($resource, $localStorage, $http, dbaasConfig, $location) {
    function clearToken() {
        user.token = '';
        delete $http.defaults.headers.common['Authorization'];
        updateUserStorage();
    }

    function setToken(token) {
        user.token = token;
        updateUserStorage();
        $http.defaults.headers.common['Authorization'] = 'Token ' + token;
    }

    function updateUserStorage() {
        $localStorage.user = user;
    }

    function updateUserVoice() {
        /*global UserVoice:false */
        if (typeof UserVoice !== 'undefined') {
            UserVoice.push(['identify', {
                email: user.email,
                account: {
                    name: user.email,
                    plan: user.is_paid ? 'Paid' : 'Free'
                }
            }]);
        }
        window.userEmail = user.email;
    }

    function initialize() {
        $http.defaults.headers.common['Authorization'] = 'Token ' + user.token;
        updateUserVoice();
    }

    function setUser(aUser) {
        user.isPaid = aUser.is_paid;
        user.email = aUser.email;
        user.firstName = aUser.first_name;
        user.lastName = aUser.last_name;
        identityConfirmed = true;
        updateUserStorage();
        updateUserVoice();
    }

    function checkIdentity() {
        return Identity.get({}, function (data) {
            setUser(data);
        });
    }


    var Registration = $resource(dbaasConfig.registerUrlEscaped + ':activation_code', {activation_code: '@activation_code'}, {
        activate: {method: 'PUT'},
        reminder: {method: 'GET'}
    });
    var Token = $resource(dbaasConfig.authUrlEscaped + '/:id', {id: '@id'});
    var Identity = $resource(dbaasConfig.apiUrlEscaped + 'self');
    var identityConfirmed = false;

    var user = $localStorage.$default({user: {email: "", isPaid: false, token: undefined}}).user;


    if (user.token) {
        initialize();
    }

    return {
        user: user,
        register: function (email) {
            clearToken();
            return Registration.save({email: email});
        },
        checkActivation: function (activationCode) {
            clearToken();
            return Registration.get({activation_code: activationCode});
        },
        activate: function (activationCode, password) {
            clearToken();
            return Registration.activate({activation_code: activationCode}, {password: password});
        },
        reminder: function (email) {
            return Registration.reminder({email: email});
        },
        login: function (email, password) {
            user.email = email;
            clearToken();
            return Token.save({username: email, password: password}, function (data) {
                setToken(data.token);
                checkIdentity();
            });
        },
        identify: function (forceCheck) {
            forceCheck = typeof forceCheck !== 'undefined' ? forceCheck : false;

            if (!identityConfirmed || forceCheck) {
                return checkIdentity();
            }
            return null;
        },
        logout: function () {
            clearToken();
            $location.path("/");
        },
        setToken: function (token) {
            setToken(token);
        }
    };
});