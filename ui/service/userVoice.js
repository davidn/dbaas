angular.module('geniedb').factory('userVoice', function (dbaasConfig, User, growl) {

    var userVoice = {
        contact: function (subject, message) {
            // Note: UserVoice specifically uses this library (JSONP) which has a different dialect from Angular JSONP
            $.jsonp({
                url: 'https://' + dbaasConfig.userVoiceSubdomain + '.uservoice.com/api/v1/tickets/create_via_jsonp.json?callback=?',
                data: {
                    client: dbaasConfig.userVoiceClientKey,
                    ticket: {
                        message: message,
                        subject: subject
                    },
                    email: User.user.email
                },
                success: function (data) {
                    growl.success({body: 'Your request has been submitted, we will follow-up within one business day.', timeOut: 10000});
                },
                error: function (d, msg) {
                    growl.error({body: 'Unable to submit request.  Please try again.'});
                }
            });
        }
    };

    return userVoice;
});
