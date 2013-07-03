// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// the compiled file.
//
// WARNING: THE FIRST BLANK LINE MARKS THE END OF WHAT'S TO BE PROCESSED, ANY BLANK LINE SHOULD
// GO AFTER THE REQUIRES BELOW.
//
//= require jquery
//= require jquery_ujs
//= require twitter/bootstrap
//= require_tree .

$(document).ready(function() {

	if($('#db_instance_backup_window_no_preference').is(":checked")){
		$("div#backup_window_container select").removeAttr("disabled")
	}

	if($("#db_instance_backup_window_select_window").is(":checked")){
		$("div#backup_window_container").show();
	}

	$(".backup_window_wrapper input:radio:eq(0)").click(function(){
		$("div#backup_window_container").show(100);
		$("div#backup_window_container select").removeAttr("disabled")
	});
	
	$(".backup_window_wrapper input:radio:eq(1)").click(function(){
		$("div#backup_window_container").hide(100);
		$("div#backup_window_container select").attr("disabled", "disabled")
		$("div#backup_window_container select :selected").each(function(){
			$(this).removeAttr("selected")
		})
	});

	$("[rel='tooltip']").tooltip();
	
});
