describe('BillinginfoCtrl', function() {

	beforeEach(module('geniedb'));

	var scope,ctrl;

    beforeEach(inject(function($rootScope, $controller) {
      scope = $rootScope.$new();
      ctrl = $controller('BillinginfoCtrl', {$scope: scope});
    }));	

	it('should ...', inject(function() {

		expect(1).toEqual(1);
		
	}));

});