/*jshint globalstrict: true*/

var endpoint = 'https://dbaas.geniedb.com:4000/api/';
var auth_endpoint = 'https://dbaas.geniedb.com:4000/api-token-auth/';
var token = '2f29d5f9ce21ab4b297d725c449ad4873a7e9edf';
var username = 'ETW_International';

if (typeof(Storage) !== "undefined") {
    var t = localStorage.getItem('token');
    if (t !== null) {
//        token = t;
}
t = localStorage.getItem('username');
if (t !== null) {
    username = t;
}
}


function api_call(method, path, object, success, error) {
    var headers = token == '' ? {} : {Authorization: 'Token ' + token};
    $.ajax(path.indexOf('http') == 0 ? path : endpoint + path, {
        type: method,
        contentType: 'application/json',
        success: success,
        error: error,
        data: JSON.stringify(object),
        dataType: 'json',
        headers: headers
    });
}

function generic_error(xhr, status, error) {
    //$("#main").prepend('<div class="alert alert-block alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><h4 class="alert-heading">Error: ' + status + '</h4><p>' + error + '</p></div>');
    console.log(status, error);
    $('#alertBody').html(error);
    $('#alertModal').modal('show');
}

function onRefresh() {
    api_call('GET', 'clusters/', {}, display_clusters, generic_error);
}

function generic_success(data, status, xhr) {
    onRefresh();
}

function onAddCluster(e) {
    console.log('onAddCluster');
    api_call('POST', 'clusters/', {
        dbname: $("#db_name").val(),
        dbusername: $("#master_username").val(),
        dbpassword: $("#master_password").val(),
        port: $("#port").val()
    },
    function (data, status, xhr) {
        $("#addCluster").modal('hide');
        onRefresh();
    },
    generic_error);
}

function onNodeAdd(e) {
    addNodes(e.currentTarget.getAttribute('data-cluster'));
    //generic_error(null, 'unsupported', 'Adding a node to an existing cluster is currently unsupported');
}

function onLaunchCluster(e) {
    $(e.currentTarget).button('loading');
    api_call('POST', e.currentTarget.getAttribute('data-cluster') + 'launch_all/', {}, function (data, status, xhr) {
        $(e.currentTarget).button('reset');
        generic_success(data, status, xhr);
    }, generic_error);
}

function onClusterDelete(e) {
    api_call('DELETE', e.currentTarget.getAttribute('data-cluster'), {}, generic_success, generic_error);
}

function getNodeUrlFromMenu(menuTag){
    return $(menuTag).closest('tr').attr('data-node');
}

function onNodeDelete(e) {
    api_call('DELETE', getNodeUrlFromMenu(e.currentTarget), {}, generic_success, generic_error);
}

function onNodePause(e) {
    api_call('POST', getNodeUrlFromMenu(e.currentTarget) + 'pause/', {}, generic_success, generic_error);
}

function onNodeResume(e) {
    api_call('POST', getNodeUrlFromMenu(e.currentTarget) + 'resume/', {}, generic_success, generic_error);
}

function onNodeClone(e) {
    // TODO: Display add node panel with copy of current
}
function onNodeUpgrade(e) {
    // TODO: Display upgrade panel
}
function onNodeStats(e) {
    // TODO: Display stats panel
}

function getFlavorByCode(flavors, code) {
    return flavors.filter(function (obj) {
        return obj.code === code;
    })[ 0 ];
}

function getProviderByFlavor(flavor) {
    return providers.filter(function (obj) {
        return getFlavorByCode(obj.flavors, flavor);
    })[ 0 ];
}

var statuses = [
{code: 'initial', label: 'not yet started'},
{code: 'provisioning', label: 'Provisioning Instances'},
{code: 'installing_cf', label: 'Installing GenieDB CloudFabric'},
{code: 'running', label: 'running'},
{code: 'paused', label: 'paused'},
{code: 'shutting_down', label: 'shutting down'},
{code: 'over', label: 'over'},
{code: 'error', label: 'An error occurred'}
];

function getStatusCode(statusLabel) {
    return statuses.filter(function (status) {
        return status.label === statusLabel;
    })[0].code;
}

/* TODO Remove mock stats */
function getRandomizer(bottom, top) {
    return function () {
        return Math.floor(Math.random() * ( 1 + top - bottom )) + bottom;
    }
}
function mockStats(max) {
    var randomizer = getRandomizer(0, max);

    var results = [];
    for (var i = 0; i < 60; i++) {
        results.push(randomizer());
    }
    return results;
}
function lookupNodeData(data) {
    data.forEach(function (node, i, arr) {
        node.label = node.label ? node.label : node.region ? node.region : 'Node' + i;
        node.provider = getProviderByFlavor(node.flavor);
        node.statusClass = 'node-status-' + getStatusCode(node.status);
        node.cpu = mockStats(100);
        node.iops = mockStats(10000);
    });
    return data;
}
function lookupClusterData(data) {
    data.forEach(function (cluster, i, arr) {
        lookupNodeData(cluster.nodes);
        cluster.canLaunch = true;
    });
    return data;
}

function display_clusters(data, status, xhr) {
    $("#home-div").remove();

    $("#main").markup("home", {username: username, clusters: lookupClusterData(data), providers: providers});
    activateMarkup();

    $("#refresh").off("click").on("click", onRefresh);
    $("#logout").off("click").on("click", onLogout);
    $("#add-cluster").off("click").on("click", onAddCluster);
    $(".launch-cluster").off("click").on("click", onLaunchCluster);
    $(".delete-cluster").off("click").on("click", onClusterDelete);


    $(".add-node").off("click").on("click", onNodeAdd);

    $(".node-delete").off("click").on("click", onNodeDelete);
    $(".node-pause").off("click").on("click", onNodePause);
    $(".node-resume").off("click").on("click", onNodeResume);
    $(".node-clone").off("click").on("click", onNodeClone);
    $(".node-upgrade").off("click").on("click", onNodeUpgrade);
    $(".node-stats").off("click").on("click", onNodeStats);


    $("#quickstart").on("click", onQuickStart);
}

function login_callback(data, status, xhr) {
    token = data.token;
    localStorage.setItem('token', token);
    $("#login-div").remove();
    api_call('GET', 'providers/', {}, function (data, status, xhr) {
        providers = data;
        onRefresh();
    }, register_error);
}

function login_error(xhr, status, error) {
    $("#login-fail").show();
}
function register_error(xhr, status, error) {
    $("#register-fail").show();
}

function onRegister(e) {
    e.preventDefault();
    api_call('POST', 'users/', {username: $("#username").val(), password: $("#password").val()}, login, register_error);
}

function onLogin(e) {
    e.preventDefault();
    login();
}

function login() {
    $.ajax(auth_endpoint, {
        type: 'POST',
        contentType: 'application/json',
        success: login_callback,
        error: login_error,
        data: JSON.stringify({
            username: $("#username").val(),
            password: $("#password").val()
        }),
        dataType: 'json'
    });
    username = $("#username").val();
    localStorage.setItem('username', username);
}

function generateKey(length) {
    return (Math.PI * Math.max(0.01, Math.random())).toString(36).substr(2, length);
}

function onQuickStart(e) {
    api_call('POST', 'clusters/', {
        dbname: "quickstart",
        dbusername: "appuser",
        dbpassword: generateKey(10),
        port: 3306
    }, function (data, status, xhr) {
        var nodes = [
        {    region: "sa-east-1",
        flavor: "m1.small",
        storage: 10},
        {    region: "ap-northeast-1",
        flavor: "m1.small",
        storage: 10},
        {region: "eu-west-1",
        flavor: "m1.small",
        storage: 10}
        ];
        api_call('POST', data.url, nodes, function (data2, status2, xhr2) {
            $("#launch").modal('hide');
            $(e.currentTarget).button('reset');
            generic_success(data2, status2, xhr2);
        }, generic_error);
    }, generic_error);
}

function addNodes(url){
    var nodes = [
    {    region: "sa-east-1",
    flavor: "m1.small",
    storage: 10},
    {    region: "ap-northeast-1",
    flavor: "m1.small",
    storage: 10},
    {region: "eu-west-1",
    flavor: "m1.small",
    storage: 10}
    ];
    api_call('POST', url, nodes, function (data2, status2, xhr2) {       
        generic_success(data2, status2, xhr2);
    }, generic_error);
}

function onLogout(e) {
    $("#home-div").remove();
    token = '';
    username = '';
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    $("#main").markup("login");
    activateMarkup();

    $("#login-submit").on("click", onLogin);
    $("#login-register").on("click", onRegister);
}

var providers = [];

function activateMarkup() {
    if ($("[rel=tooltip]").length) {
        $("[rel=tooltip]").tooltip();
    }
    $('.dropdown-toggle').dropdownHover();
    $('.inlinesparkline').sparkline();

}

$(function () {
    $.fn.sparkline.defaults.common.lineColor = '#8e8e8e';
    $.fn.sparkline.defaults.common.fillColor = undefined;

    activateMarkup();

    $.markup.load(function () {
        if (token == '') {
            $("#main").markup("login");
            activateMarkup();
            $("#login-submit").on("click", onLogin);
            $("#login-register").on("click", onRegister);
        } else {
            api_call('GET', 'providers/', {}, function (data, status, xhr) {
                providers = data;
                onRefresh();
            }, register_error);
        }
    });
});