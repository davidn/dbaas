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


$(function() {
	var select = $( "#instance-cpu" );
	var slider = $( "<div id='slider'></div>" ).insertAfter( select ).slider({
		min: 1,
		max: 5,
		range: "min",
		value: select[ 0 ].selectedIndex + 1,
		slide: function( event, ui ) {
			select[ 0 ].selectedIndex = ui.value - 1;
		}
	});
	$( "#instance-cpu" ).change(function() {
		slider.slider( "value", this.selectedIndex + 1 );
	});
});

$(function() {
	var select = $( "#instance-ram" );
	var slider = $( "<div id='slider'></div>" ).insertAfter( select ).slider({
		min: 1,
		max: 5,
		range: "min",
		value: select[ 0 ].selectedIndex + 1,
		slide: function( event, ui ) {
			select[ 0 ].selectedIndex = ui.value - 1;
		}
	});
	$( "#instance-ram" ).change(function() {
		slider.slider( "value", this.selectedIndex + 1 );
	});
});