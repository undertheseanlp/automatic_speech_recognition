window.app.directive('html5vfix', function () {
    return {
        restrict: 'AE',
        replace: true,
        link: function (scope, element, attrs) {
            attr_ = attrs;
            scope_ = scope;
            attrs.$set('src', attrs.nsrc);
            attrs.$observe('nsrc', function (value) {
                console.log(value);
                attr_.$set('src', value);
            })
        }
    }
});
window.app.filter('trusted', ['$sce', function ($sce) {
    return function (url) {
        return $sce.trustAsResourceUrl(url);
    };
}]);

window.app.directive('audios', function($sce) {
  return {
    restrict: 'A',
    scope: { url:'=' },
    replace: true,
    template: '<audio ng-src="{{src}}" controls></audio>',
    link: function (scope) {
        scope.$watch('url', function (newVal, oldVal) {
           if (newVal !== undefined) {
               scope.src = $sce.trustAsResourceUrl(newVal);
           }
        });
    }
  };
});
window.app.controller('SpeechRecognitionController', function ($scope, $http) {
    $http.get("speechrecognition.json")
        .then(function (result) {
            var data = result["data"];
            var items = [];
            for (var i = 0; i < data.texts_test.length; i++) {
                var item = {
                    "actual": data.texts_test[i],
                    "pred": data.texts_pred[i],
                    "wav": data.wavs_test[i],
                    "correct": data.texts_test[i] == data.texts_pred[i]
                };
                items.push(item);
            }
            $scope.items = items;
            $scope.filteredItems = $scope.items;
        });

    $scope.updateItems = function (result) {
        $scope.filteredItems = _.filter($scope.items, function (item) {
            return item.correct == result;
        })
        console.log(0);
    }
});
