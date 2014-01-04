angular.module('geniedb').controller('BillinginfoCtrl', function ($scope, $location, User, growl) {
    // TODO: Fix country encoding
    $scope.countries = [
        {"name": "Afghanistan", "code": "AF"},
        {"name": "Aland Islands", "code": "AX"},
        {"name": "Albania", "code": "AL"},
        {"name": "Algeria", "code": "DZ"},
        {"name": "American Samoa", "code": "AS"},
        {"name": "Andorra", "code": "AD"},
        {"name": "Angola", "code": "AO"},
        {"name": "Anguilla", "code": "AI"},
        {"name": "Antarctica", "code": "AQ"},
        {"name": "Antigua and Barbuda", "code": "AG"},
        {"name": "Argentina", "code": "AR"},
        {"name": "Armenia", "code": "AM"},
        {"name": "Aruba", "code": "AW"},
        {"name": "Australia", "code": "AU"},
        {"name": "Austria", "code": "AT"},
        {"name": "Azerbaijan", "code": "AZ"},
        {"name": "Bahamas", "code": "BS"},
        {"name": "Bahrain", "code": "BH"},
        {"name": "Bangladesh", "code": "BD"},
        {"name": "Barbados", "code": "BB"},
        {"name": "Belarus", "code": "BY"},
        {"name": "Belgium", "code": "BE"},
        {"name": "Belize", "code": "BZ"},
        {"name": "Benin", "code": "BJ"},
        {"name": "Bermuda", "code": "BM"},
        {"name": "Bhutan", "code": "BT"},
        {"name": "Bolivia, Plurinational State of", "code": "BO"},
        {"name": "Bonaire, Sint Eustatius and Saba", "code": "BQ"},
        {"name": "Bosnia and Herzegovina", "code": "BA"},
        {"name": "Botswana", "code": "BW"},
        {"name": "Bouvet Island", "code": "BV"},
        {"name": "Brazil", "code": "BR"},
        {"name": "British Indian Ocean Territory", "code": "IO"},
        {"name": "Brunei Darussalam", "code": "BN"},
        {"name": "Bulgaria", "code": "BG"},
        {"name": "Burkina Faso", "code": "BF"},
        {"name": "Burundi", "code": "BI"},
        {"name": "Cambodia", "code": "KH"},
        {"name": "Cameroon", "code": "CM"},
        {"name": "Canada", "code": "CA"},
        {"name": "Cape Verde", "code": "CV"},
        {"name": "Cayman Islands", "code": "KY"},
        {"name": "Central African Republic", "code": "CF"},
        {"name": "Chad", "code": "TD"},
        {"name": "Chile", "code": "CL"},
        {"name": "China", "code": "CN"},
        {"name": "Christmas Island", "code": "CX"},
        {"name": "Cocos (Keeling) Islands", "code": "CC"},
        {"name": "Colombia", "code": "CO"},
        {"name": "Comoros", "code": "KM"},
        {"name": "Congo", "code": "CG"},
        {"name": "Congo, the Democratic Republic of the", "code": "CD"},
        {"name": "Cook Islands", "code": "CK"},
        {"name": "Costa Rica", "code": "CR"},
        {"name": "Cote d'Ivoire", "code": "CI"},
        {"name": "Croatia", "code": "HR"},
        {"name": "Cuba", "code": "CU"},
        {"name": "Curacao", "code": "CW"},
        {"name": "Cyprus", "code": "CY"},
        {"name": "Czech Republic", "code": "CZ"},
        {"name": "Denmark", "code": "DK"},
        {"name": "Djibouti", "code": "DJ"},
        {"name": "Dominica", "code": "DM"},
        {"name": "Dominican Republic", "code": "DO"},
        {"name": "Ecuador", "code": "EC"},
        {"name": "Egypt", "code": "EG"},
        {"name": "El Salvador", "code": "SV"},
        {"name": "Equatorial Guinea", "code": "GQ"},
        {"name": "Eritrea", "code": "ER"},
        {"name": "Estonia", "code": "EE"},
        {"name": "Ethiopia", "code": "ET"},
        {"name": "Falkland Islands (Malvinas)", "code": "FK"},
        {"name": "Faroe Islands", "code": "FO"},
        {"name": "Fiji", "code": "FJ"},
        {"name": "Finland", "code": "FI"},
        {"name": "France", "code": "FR"},
        {"name": "French Guiana", "code": "GF"},
        {"name": "French Polynesia", "code": "PF"},
        {"name": "French Southern Territories", "code": "TF"},
        {"name": "Gabon", "code": "GA"},
        {"name": "Gambia", "code": "GM"},
        {"name": "Georgia", "code": "GE"},
        {"name": "Germany", "code": "DE"},
        {"name": "Ghana", "code": "GH"},
        {"name": "Gibraltar", "code": "GI"},
        {"name": "Greece", "code": "GR"},
        {"name": "Greenland", "code": "GL"},
        {"name": "Grenada", "code": "GD"},
        {"name": "Guadeloupe", "code": "GP"},
        {"name": "Guam", "code": "GU"},
        {"name": "Guatemala", "code": "GT"},
        {"name": "Guernsey", "code": "GG"},
        {"name": "Guinea", "code": "GN"},
        {"name": "Guinea-Bissau", "code": "GW"},
        {"name": "Guyana", "code": "GY"},
        {"name": "Haiti", "code": "HT"},
        {"name": "Heard Island and McDonald Islands", "code": "HM"},
        {"name": "Holy See (Vatican City State)", "code": "VA"},
        {"name": "Honduras", "code": "HN"},
        {"name": "Hong Kong", "code": "HK"},
        {"name": "Hungary", "code": "HU"},
        {"name": "Iceland", "code": "IS"},
        {"name": "India", "code": "IN"},
        {"name": "Indonesia", "code": "ID"},
        {"name": "Iran, Islamic Republic of", "code": "IR"},
        {"name": "Iraq", "code": "IQ"},
        {"name": "Ireland", "code": "IE"},
        {"name": "Isle of Man", "code": "IM"},
        {"name": "Israel", "code": "IL"},
        {"name": "Italy", "code": "IT"},
        {"name": "Jamaica", "code": "JM"},
        {"name": "Japan", "code": "JP"},
        {"name": "Jersey", "code": "JE"},
        {"name": "Jordan", "code": "JO"},
        {"name": "Kazakhstan", "code": "KZ"},
        {"name": "Kenya", "code": "KE"},
        {"name": "Kiribati", "code": "KI"},
        {"name": "Korea, Democratic People's Republic of", "code": "KP"},
        {"name": "Korea, Republic of", "code": "KR"},
        {"name": "Kuwait", "code": "KW"},
        {"name": "Kyrgyzstan", "code": "KG"},
        {"name": "Lao People's Democratic Republic", "code": "LA"},
        {"name": "Latvia", "code": "LV"},
        {"name": "Lebanon", "code": "LB"},
        {"name": "Lesotho", "code": "LS"},
        {"name": "Liberia", "code": "LR"},
        {"name": "Libya", "code": "LY"},
        {"name": "Liechtenstein", "code": "LI"},
        {"name": "Lithuania", "code": "LT"},
        {"name": "Luxembourg", "code": "LU"},
        {"name": "Macao", "code": "MO"},
        {"name": "Macedonia, the former Yugoslav Republic of", "code": "MK"},
        {"name": "Madagascar", "code": "MG"},
        {"name": "Malawi", "code": "MW"},
        {"name": "Malaysia", "code": "MY"},
        {"name": "Maldives", "code": "MV"},
        {"name": "Mali", "code": "ML"},
        {"name": "Malta", "code": "MT"},
        {"name": "Marshall Islands", "code": "MH"},
        {"name": "Martinique", "code": "MQ"},
        {"name": "Mauritania", "code": "MR"},
        {"name": "Mauritius", "code": "MU"},
        {"name": "Mayotte", "code": "YT"},
        {"name": "Mexico", "code": "MX"},
        {"name": "Micronesia, Federated States of", "code": "FM"},
        {"name": "Moldova, Republic of", "code": "MD"},
        {"name": "Monaco", "code": "MC"},
        {"name": "Mongolia", "code": "MN"},
        {"name": "Montenegro", "code": "ME"},
        {"name": "Montserrat", "code": "MS"},
        {"name": "Morocco", "code": "MA"},
        {"name": "Mozambique", "code": "MZ"},
        {"name": "Myanmar", "code": "MM"},
        {"name": "Namibia", "code": "NA"},
        {"name": "Nauru", "code": "NR"},
        {"name": "Nepal", "code": "NP"},
        {"name": "Netherlands", "code": "NL"},
        {"name": "New Caledonia", "code": "NC"},
        {"name": "New Zealand", "code": "NZ"},
        {"name": "Nicaragua", "code": "NI"},
        {"name": "Niger", "code": "NE"},
        {"name": "Nigeria", "code": "NG"},
        {"name": "Niue", "code": "NU"},
        {"name": "Norfolk Island", "code": "NF"},
        {"name": "Northern Mariana Islands", "code": "MP"},
        {"name": "Norway", "code": "NO"},
        {"name": "Oman", "code": "OM"},
        {"name": "Pakistan", "code": "PK"},
        {"name": "Palau", "code": "PW"},
        {"name": "Palestinian Territory, Occupied", "code": "PS"},
        {"name": "Panama", "code": "PA"},
        {"name": "Papua New Guinea", "code": "PG"},
        {"name": "Paraguay", "code": "PY"},
        {"name": "Peru", "code": "PE"},
        {"name": "Philippines", "code": "PH"},
        {"name": "Pitcairn", "code": "PN"},
        {"name": "Poland", "code": "PL"},
        {"name": "Portugal", "code": "PT"},
        {"name": "Puerto Rico", "code": "PR"},
        {"name": "Qatar", "code": "QA"},
        {"name": "Reunion", "code": "RE"},
        {"name": "Romania", "code": "RO"},
        {"name": "Russian Federation", "code": "RU"},
        {"name": "Rwanda", "code": "RW"},
        {"name": "Saint Barthelemy", "code": "BL"},
        {"name": "Saint Helena, Ascension and Tristan da Cunha", "code": "SH"},
        {"name": "Saint Kitts and Nevis", "code": "KN"},
        {"name": "Saint Lucia", "code": "LC"},
        {"name": "Saint Martin (French part)", "code": "MF"},
        {"name": "Saint Pierre and Miquelon", "code": "PM"},
        {"name": "Saint Vincent and the Grenadines", "code": "VC"},
        {"name": "Samoa", "code": "WS"},
        {"name": "San Marino", "code": "SM"},
        {"name": "Sao Tome and Principe", "code": "ST"},
        {"name": "Saudi Arabia", "code": "SA"},
        {"name": "Senegal", "code": "SN"},
        {"name": "Serbia", "code": "RS"},
        {"name": "Seychelles", "code": "SC"},
        {"name": "Sierra Leone", "code": "SL"},
        {"name": "Singapore", "code": "SG"},
        {"name": "Sint Maarten (Dutch part)", "code": "SX"},
        {"name": "Slovakia", "code": "SK"},
        {"name": "Slovenia", "code": "SI"},
        {"name": "Solomon Islands", "code": "SB"},
        {"name": "Somalia", "code": "SO"},
        {"name": "South Africa", "code": "ZA"},
        {"name": "South Georgia and the South Sandwich Islands", "code": "GS"},
        {"name": "South Sudan", "code": "SS"},
        {"name": "Spain", "code": "ES"},
        {"name": "Sri Lanka", "code": "LK"},
        {"name": "Sudan", "code": "SD"},
        {"name": "Suriname", "code": "SR"},
        {"name": "Svalbard and Jan Mayen", "code": "SJ"},
        {"name": "Swaziland", "code": "SZ"},
        {"name": "Sweden", "code": "SE"},
        {"name": "Switzerland", "code": "CH"},
        {"name": "Syrian Arab Republic", "code": "SY"},
        {"name": "Taiwan, Province of China", "code": "TW"},
        {"name": "Tajikistan", "code": "TJ"},
        {"name": "Tanzania, United Republic of", "code": "TZ"},
        {"name": "Thailand", "code": "TH"},
        {"name": "Timor-Leste", "code": "TL"},
        {"name": "Togo", "code": "TG"},
        {"name": "Tokelau", "code": "TK"},
        {"name": "Tonga", "code": "TO"},
        {"name": "Trinidad and Tobago", "code": "TT"},
        {"name": "Tunisia", "code": "TN"},
        {"name": "Turkey", "code": "TR"},
        {"name": "Turkmenistan", "code": "TM"},
        {"name": "Turks and Caicos Islands", "code": "TC"},
        {"name": "Tuvalu", "code": "TV"},
        {"name": "Uganda", "code": "UG"},
        {"name": "Ukraine", "code": "UA"},
        {"name": "United Arab Emirates", "code": "AE"},
        {"name": "United Kingdom", "code": "GB"},
        {"name": "United States", "code": "US"},
        {"name": "United States Minor Outlying Islands", "code": "UM"},
        {"name": "Uruguay", "code": "UY"},
        {"name": "Uzbekistan", "code": "UZ"},
        {"name": "Vanuatu", "code": "VU"},
        {"name": "Venezuela, Bolivarian Republic of", "code": "VE"},
        {"name": "Viet Nam", "code": "VN"},
        {"name": "Virgin Islands, British", "code": "VG"},
        {"name": "Virgin Islands, U.S.", "code": "VI"},
        {"name": "Wallis and Futuna", "code": "WF"},
        {"name": "Western Sahara", "code": "EH"},
        {"name": "Yemen", "code": "YE"},
        {"name": "Zambia", "code": "ZM"},
        {"name": "Zimbabwe", "code": "ZW"}
    ];

    $scope.cc = {billing_address:{}};
    $scope.mode = 'address';
    $scope.cancel = function () {
        $location.path("/upgrade");
    };

    $scope.showPayment = function () {
        $scope.mode = 'payment';
    };

    $scope.showAddress = function () {
        $scope.mode = 'address';
    };

    $scope.save = function () {
        $scope.isLoading = true;
        var cc = angular.copy($scope.cc);
        cc.expire_year = '20' + cc.expire_year;
        cc.type = creditCardTypeFromNumber(cc.number);
        User.billing(cc).success(function () {
            growl.success({body: 'Account Successfully Upgraded'});
            $location.path("/list");
        }).error(handleError);
    };

    function handleError(err) {
        $scope.isLoading = false;
        if (err && err.data && err.data.detail) {
            growl.error({body: err.data.detail});
        } else if (err && err.data && err.data.non_field_errors && err.data.non_field_errors[0]) {
            growl.error({body: err.data.non_field_errors[0]});
        } else {
            growl.error({body: 'Error processing Credit Card, please try again'});
        }
    }

    function creditCardTypeFromNumber(num) {
        num = num.replace(/[^\d]/g, '');
        if (num.match(/^5[1-5]\d{14}$/)) {
            return 'mastercard';
        } else if (num.match(/^4\d{15}/) || num.match(/^4\d{12}/)) {
            return 'visa';
        } else if (num.match(/^3[47]\d{13}/)) {
            return 'amex';
        } else if (num.match(/^6011\d{12}/)) {
            return 'discover';
        }
        return 'UNKNOWN';
    }


    //Form Validation
    var billingFormWatch = '(!billingForm.firstName.$focused && billingForm.firstName.$dirty && (billingForm.firstName.$invalid || billingForm.firstName.$error.required)) ||' +
        ' (!billingForm.lastName.$focused && billingForm.lastName.$dirty && (billingForm.lastName.$invalid || billingForm.lastName.$error.required)) ||' +
        ' (!billingForm.billingAddressLine.$focused && billingForm.billingAddressLine.$dirty && (billingForm.billingAddressLine.$invalid || billingForm.billingAddressLine.$error.required)) ||' +
        ' (!billingForm.billingAddressCity.$focused && billingForm.billingAddressCity.$dirty && (billingForm.billingAddressCity.$invalid || billingForm.billingAddressCity.$error.required)) ||' +
        ' (!billingForm.billingAddressState.$focused && billingForm.billingAddressState.$dirty && (billingForm.billingAddressState.$invalid || billingForm.billingAddressState.$error.required)) ||' +
        ' (!billingForm.billingAddressPostalCode.$focused && billingForm.billingAddressPostalCode.$dirty && (billingForm.billingAddressPostalCode.$invalid || billingForm.billingAddressPostalCode.$error.required)) ||' +
        ' (billingAddressCountryCode.$dirty && !cc.billing_address.country_code)';
    var paymentFormWatch = '(!paymentForm.ccNumber.$focused && paymentForm.ccNumber.$dirty && (paymentForm.ccNumber.$invalid || paymentForm.ccNumber.$error.required)) ||' +
        '(!paymentForm.ccExpMonth.$focused && paymentForm.ccExpMonth.$dirty && (paymentForm.ccExpMonth.$invalid || paymentForm.ccExpMonth.$error.required)) ||' +
        '(!paymentForm.ccExpYear.$focused && paymentForm.ccExpYear.$dirty && (paymentForm.ccExpYear.$invalid || paymentForm.ccExpYear.$error.required)) ||' +
        '(!paymentForm.ccv2.$focused && paymentForm.ccv2.$dirty && (paymentForm.ccv2.$invalid || paymentForm.ccv2.$error.required))';
    $scope.showBillingValidationErrors = false;
    $scope.showPaymentValidationErrors = false;
    $scope.billingValidationError = '';
    $scope.paymentValidationError = '';
    $scope.$watch(billingFormWatch, function(newVal, oldVal){
        if(newVal !== oldVal) {
            $scope.showBillingValidationErrors = newVal;
            if(newVal) {
                if($scope.billingForm.firstName.$invalid || $scope.billingForm.firstName.$error.required) {
                    $scope.billingValidationError = 'First Name cannot be empty';
                } else if($scope.billingForm.lastName.$invalid || $scope.billingForm.lastName.$error.required) {
                    $scope.billingValidationError = 'Last Name cannot be empty';
                } else if($scope.billingForm.billingAddressLine.$invalid || $scope.billingForm.billingAddressLine.$error.required) {
                    $scope.billingValidationError = 'Street Address cannot be empty';
                } else if($scope.billingForm.billingAddressCity.$invalid || $scope.billingForm.billingAddressCity.$error.required) {
                    $scope.billingValidationError = 'City cannot be empty';
                } else if($scope.billingForm.billingAddressState.$invalid || $scope.billingForm.billingAddressState.$error.required) {
                    $scope.billingValidationError = 'State cannot be empty';
                } else if($scope.billingForm.billingAddressPostalCode.$invalid || $scope.billingForm.billingAddressPostalCode.$error.required) {
                    $scope.billingValidationError = 'Postal Code cannot be empty';
                } else if(!$scope.billingAddressCountryCode) {
                    $scope.billingValidationError = 'Country cannot be empty';
                } else {
                    $scope.billingValidationError = '';
                }
            }
        }
    }, true);

    $scope.$watch(paymentFormWatch, function(newVal, oldVal){
        if(newVal !== oldVal) {
            $scope.showPaymentValidationErrors = newVal;
            if(newVal) {
                if($scope.paymentForm.ccNumber.$invalid || $scope.paymentForm.ccNumber.$error.required) {
                    $scope.paymentValidationError = 'Card Number cannot be empty';
                } else if($scope.paymentForm.ccExpMonth.$invalid || $scope.paymentForm.ccExpMonth.$error.required) {
                    $scope.paymentValidationError = 'Invalid Month';
                } else if($scope.paymentForm.ccExpYear.$invalid || $scope.paymentForm.ccExpYear.$error.required) {
                    $scope.paymentValidationError = 'Invalid Year';
                } else if($scope.paymentForm.ccv2.$invalid || $scope.paymentForm.ccv2.$error.required) {
                    $scope.paymentValidationError = 'CCV2 cannot be empty';
                } else {
                    $scope.paymentValidationError = '';
                }
            }
        }
    }, true);
});
