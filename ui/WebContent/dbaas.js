
var endpoint = 'http://localhost:8000/api/';
var auth_endpoint = 'http://localhost:8000/api-token-auth/';
var token = '';
var username = '';

if(typeof(Storage)!=="undefined") {
	t = localStorage.getItem('token');
	if (t != null) {
		token = t;
	}
	t = localStorage.getItem('username');
	if (t != null) {
		username = t;
	}
}

function api_call(method, path, object, success, error) {
	var headers = token == '' ? {}: {Authorization: 'Token '+token};
	$.ajax(path.indexOf('https://')==0?path:endpoint+path, {
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
	api_call('POST', 'clusters/', {
			dbname: $("#db_name").val(),
			dbusername: $("#master_username").val(),
			dbpassword: $("#master_password").val(),
			port: $("#port").val()
		},
		function (data, status, xhr) {
		var nodes = [];
			$.each(providers, function(i, provider) {
				$.each(provider.regions, function(j, region) {
					var node = {
							region: region.code,
							flavor: $("#"+provider.code+"_flavor").val(),
							storage: $("#allocated_storage").val()
					};
					if ($("#provision_iops").is(':checked')) {
						node.iops = $("#iops").val();
					}
					for (var k= 0; k < $("#"+region.code+"_count").val(); k++) {
						nodes.push(node);
					}
				})
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
		},
		generic_error);
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

function pause_node(e) {
	$(e.currentTarget).button('loading');
	api_call('POST', e.currentTarget.getAttribute('data-node')+'pause/', {}, generic_success, generic_error);
}

function resume_node(e) {
	$(e.currentTarget).button('loading');
	api_call('POST', e.currentTarget.getAttribute('data-node')+'resume/', {}, generic_success, generic_error);
}

function display_clusters(data, status, xhr) {
	$("#home-div").remove();
	$("#main").markup("home", {username: username, clusters: data, providers: providers});
    activateToolTips();

	setup_dialog();
	$("#refresh").on("click", refresh_home);
	$("#logout").on("click", logout);
	$("#add-cluster").off("click");
	$("#add-cluster").on("click", add_cluster);
	$(".add-node").on("click", add_node);
	$(".launch-cluster").on("click", launch_cluster);
	$(".delete-cluster").on("click", delete_cluster);
	$(".pause-node").on("click", pause_node);
	$(".resume-node").on("click", resume_node);
	$(".delete-node").on("click", delete_node);
	$(".node-box").on("click", toggle_node_details);
}

function login_callback(data, status, xhr) {
	token = data.token;
	localStorage.setItem('token',token);
	$("#login-div").remove();
	api_call('GET', 'providers/', {}, function(data, status, xhr) {
		providers = data;
		refresh_home();
	}, register_error);
}

function login_error(xhr, status, error) {
	$("#login-fail").show();
}
function register_error(xhr, status, error) {
	$("#register-fail").show();
}

function register(e) {
	e.preventDefault();
	api_call('POST', 'users/', {username: $("#username").val(), password: $("#password").val()}, login, register_error);
}

function login_button(e) {
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
	localStorage.setItem('username',username);
}

function generateKey(length){
	return (Math.PI * Math.max(0.01, Math.random())).toString(36).substr(2, length); 
}

function quickStart(e) {
	$(e.currentTarget).button('loading');
	api_call('POST', 'clusters/', {
			dbname: "quickstart",
			dbusername: "appuser",
			dbpassword: generateKey(10),
			port: 3306
		},
		function (data, status, xhr) {
		var nodes = [];
			$.each(providers, function(i, provider) {
				$.each(provider.regions, function(j, region) {
					var node = {
							region: region.code,
							flavor: $("#"+provider.code+"_flavor").val(),
							storage: $("#allocated_storage").val()
					};
					if ($("#provision_iops").is(':checked')) {
						node.iops = $("#iops").val();
					}
					for (var k= 0; k < $("#"+region.code+"_count").val(); k++) {
						nodes.push(node);
					}
				})
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
		},
		generic_error);
}






function logout(e) {
	$("#home-div").remove();
	token = '';
	username = '';
	localStorage.removeItem('token');
	localStorage.removeItem('username');
	$("#main").markup("login");
    activateToolTips();

	$("#login-submit").on("click", login_button);
	$("#login-register").on("click", register);

}

var providers = [];

function adjust_instance_types() {
	providers.forEach(function(provider, i, arr) {
		var cpus = $("#"+provider.code+"_cpu_count")[0].options[$("#"+provider.code+"_cpu_count")[0].selectedIndex].text;
		var ram = $("#"+provider.code+"_ram_amount")[0].options[$("#"+provider.code+"_ram_amount")[0].selectedIndex].text;
		var select = $("#"+provider.code+"_flavor")[0];
		for (var j = select.options.length - 1; j >= 0; j--) {
			select.remove(j);
		}
		provider.flavors.forEach(function(flavor, j, flavors) {
			if (flavor.ram == ram && flavor.cpus == cpus) {
				var opt = document.createElement("option");
				opt.text = flavor.name;
				opt.value = flavor.code;
				select.add(opt);
			}
		});
		//$("#step_two")[0].disabled = select.options.length == 0;
		if (select.options.length != 0)
			select.options.selectedIndex = 0;
	});
}

function setup_dialog() {
/*	providers.forEach(function(provider, i, arr) {
		var cpu_select = $("#"+provider.code+"_cpu_count");
		var cpu_slider = $("#"+provider.code+"_cpu_slider").slider({
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

		var ram_select = $("#"+provider.code+"_ram_amount");
		var ram_slider = $("#"+provider.code+"_ram_slider").slider({
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
	});
	adjust_instance_types();
	*/
}

$(function() {
	$.markup.load(function() {
		if (token == '') {
			$("#main").markup("login");
            activateToolTips();
			$("#login-submit").on("click", login_button);
			$("#login-register").on("click", register);
		} else {
			api_call('GET', 'providers/', {}, function(data, status, xhr) {
				providers = data;
				refresh_home();
			}, register_error);
		}
	});
});

$(document).ready(function () {
    activateToolTips();
});

function activateToolTips(){
    if ($("[rel=tooltip]").length) {
        $("[rel=tooltip]").tooltip();
    }
}
