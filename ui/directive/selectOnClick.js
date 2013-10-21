angular.module('geniedb').directive('selectOnClick', function () {
        return {
            link: function (scope, element, attrs) {
                element.bind('click', function (event) {
                    scope.$apply(function () {
                        if (document.createRange && window.getSelection) {
                            var range = document.createRange();
                            range.selectNodeContents(element.context);
                            var sel = window.getSelection();
                            sel.removeAllRanges();
                            sel.addRange(range);
                        } else if (document.selection && document.body.createTextRange) {
                            var textRange = element.context.createTextRange();
                            textRange.select();
                        }
                    });
                });
            }
        };
    }
);