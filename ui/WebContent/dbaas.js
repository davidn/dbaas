
var endpoint = 'https://dbaas.geniedb.com:4000/api/';
var auth_endpoint = 'https://dbaas.geniedb.com:4000/api-token-auth/';
var token = '';
if(typeof(Storage)!=="undefined") {
	t = localStorage.getItem('token');
	if (t != null) {
		token = t;
	}
}

function api_call(method, path, object, success, error) {
	$.ajax(path.indexOf('https://')==0?path:endpoint+path, {
		type: method,
		contentType: 'application/json',
		success: success,
		error: error,
		data: JSON.stringify(object),
		dataType: 'json',
		headers: {Authorization: 'Token '+token}
	});
}

function generic_error(xhr, status, error) {
	$("#main").prepend('<div class="alert alert-block alert-error fade in"><a class="close" data-dismiss="alert" href="#">&times;</a><h4 class="alert-heading">Error: '+status+'</h4><p>'+error+'</p></div>');
}

function toggle_node_details(e) {
	$(e.currentTarget).toggleClass("node-box-selected");
}

function refresh_home() {
	api_call('GET', 'clusters/', {}, display_clusters, generic_error);
}

function generic_success(data, status, xhr) {
	refresh_home();
}

function add_cluster(e) {
	$(e.currentTarget).button('loading');
	api_call('POST', 'clusters/', {}, function (data, status, xhr) {
		var nodes = [];
		$.each(regions, function(i, region) {
			var node = {
					region: region.name,
					size: $("#node_size").val(),
					storage: $("#allocated_storage").val(),
					databases: [$("#db_name").val()],
					username: $("#master_username").val(),
					password: $("#master_password").val(),
					port: $("#port").val()
			};
			if ($("#provision_iops").is(':checked')) {
				node.iops = $("#iops").val();
			}
			for (var i = 0; i < $("#"+region.name+"_count").val(); i++) {
				nodes.push(node);
			}
		});
		if (nodes.length > 0) {
			api_call('POST', data.url, nodes, function(data2, status2, xhr2) {
				$("#launch").modal('hide');
				$(e.currentTarget).button('reset');
				generic_success(data2, status2, xhr2);
			}, generic_error);
		} else {
			$("#launch").modal('hide');
			$(e.currentTarget).button('reset');
			refresh_home();
		}
	}, generic_error);
}

function add_node(e) {
	generic_error(null, 'unsupported', 'Adding a node to an existing cluster is currently unsupported');
}

function launch_cluster(e) {
	$(e.currentTarget).button('loading');
	api_call('POST', e.currentTarget.getAttribute('data-cluster')+'launch_all/', {}, function(data, status, xhr) {
		$(e.currentTarget).button('reset');
		generic_success(data, status, xhr);
	}, generic_error);
}

function delete_cluster(e) {
	$(e.currentTarget).button('loading');
	api_call('DELETE', e.currentTarget.getAttribute('data-cluster'), {}, generic_success, generic_error);
}

function delete_node(e) {
	$(e.currentTarget).button('loading');
	api_call('DELETE', e.currentTarget.getAttribute('data-node'), {}, generic_success, generic_error);
}

function display_clusters(data, status, xhr) {
	$("#home-div").remove();
	$("#main").markup("home", {clusters: data, instance_types: instance_types, regions: regions});
	setup_dialog();
	$("#refresh").on("click", refresh_home);
	$("#logout").on("click", logout);
	$("#add-cluster").off("click");
	$("#add-cluster").on("click", add_cluster);
	$(".add-node").on("click", add_node);
	$(".launch-cluster").on("click", launch_cluster);
	$(".delete-cluster").on("click", delete_cluster);
	$(".delete-node").on("click", delete_node);
	$(".node-box").on("click", toggle_node_details);
}

function login_callback(data, status, xhr) {
	token = data.token;
	localStorage.setItem('token',token);
	$("#login-div").remove();
	refresh_home();
}

function login_error(xhr, status, error) {
	$("#login-fail").show();
}
function register_error(xhr, status, error) {
	$("#register-fail").show();
}

function register(e) {
	e.preventDefault();
	api_call('POST', 'user/', {username: $("#username").val(), password: $("#password").val()}, login, register_error);
}

function login_callback(e) {
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
}

function logout(e) {
	$("#home-div").remove();
	token = '';
	localStorage.removeItem('token');
	$("#main").markup("login");
	$("#login-submit").on("click", login_callback);
	$("#login-register").on("click", register);
	
}

// todo fetch these dynamically
var instance_types = [
	{id : 1, cpus : 1, ram : 1, name : "t1.micro"},
	{id : 2, cpus : 1, ram : 2, name : "m1.small"},
	{id : 3, cpus : 1, ram : 4, name : "m1.medium"},
	{id : 4, cpus : 2, ram : 8, name : "m1.large"},
	{id : 5, cpus : 4, ram : 16, name : "m1.xlarge"},
	{id : 6, cpus : 4, ram : 16, name : "m3.xlarge"},
	{id : 7, cpus : 8, ram : 32, name : "m3.2xlarge"},
	{id : 8, cpus : 2, ram : 2, name : "c1.medium"},
	{id : 9, cpus : 8, ram : 8, name : "c1.xlarge"},
	{id : 10, cpus : 32, ram : 64, name : "cc2.8xlarge"},
	{id : 11, cpus : 2, ram : 16, name : "m2.xlarge"},
	{id : 12, cpus : 4, ram : 32, name : "m2.2xlarge"},
	{id : 13, cpus : 8, ram : 64, name : "m2.4xlarge"},
	{id : 14, cpus : 32, ram : 224, name : "cr1.8xlarge"},
	{id : 15, cpus : 16, ram : 64, name : "hi1.4xlarge"},
	{id : 16, cpus : 16, ram : 117, name : "hs1.8xlarge"},
	{id : 17, cpus : 32, ram : 16, name : "cg1.4xlarge"}
];

var regions = [
	{name:"us-west-1", text:"US West (N. California)"},
	{name:"us-west-2", text:"US West (Oregon)"},
	{name:"us-east-1", text:"US East (N. Virginia)"},
	{name:"eu-west-1", text:"EU (Ireland)"},
	{name:"ap-northeast-1", text:"Asia Pacific (Tokyo)"},
	{name:"ap-southeast-1", text:"Asia Pacific (Singapore)"},
	{name:"ap-southeast-2", text:"Asia Pacific (Sydney)"},
	{name:"sa-east-1", text:"South America (São Paulo)"}
];

function adjust_instance_types() {
	var cpus = $("#cpu_count")[0].options[$("#cpu_count")[0].selectedIndex].text;
	var ram = $("#ram_amount")[0].options[$("#ram_amount")[0].selectedIndex].text;
	var select = $("#node_size")[0];
	for ( var i = select.options.length - 1; i >= 0; i--) {
		select.remove(i);
	}
	instance_types.forEach(function(el, i, arr) {
		if (el.ram == ram && el.cpus == cpus) {
			opt = document.createElement("option");
			opt.text = el.name;
			opt.value = el.name;
			select.add(opt);
		}
	});
	//$("#step_two")[0].disabled = select.options.length == 0;
	if (select.options.length != 0)
		select.options.selectedIndex = 0;
}

function setup_dialog() {
	var cpu_select = $("#cpu_count");
	var cpu_slider = $("#cpu-slider").slider({
		min : 1,
		max : 4,
		range : "min",
		value : cpu_select[0].selectedIndex + 1,
		slide : function(event, ui) {
			cpu_select[0].selectedIndex = ui.value - 1;
			adjust_instance_types();
		}
	});
	cpu_select.change(function() {
		cpu_slider.slider("value", this.selectedIndex + 1);
		adjust_instance_types();
	});

	var ram_select = $("#ram_amount");
	var ram_slider = $("#ram-slider").slider({
		min : 1,
		max : 7,
		range : "min",
		value : ram_select[0].selectedIndex + 1,
		slide : function(event, ui) {
			ram_select[0].selectedIndex = ui.value - 1;
			adjust_instance_types();
		}
	});
	ram_select.change(function() {
		ram_slider.slider("value", this.selectedIndex + 1);
		adjust_instance_types();
	});
	adjust_instance_types();
}

$(function() {
	$.markup.load(function() {
		if (token == '') {
			$("#main").markup("login");
			$("#login-submit").on("click", login);
		} else {
			refresh_home();
		}
	});
});