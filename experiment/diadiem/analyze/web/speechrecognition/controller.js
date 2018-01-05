window.app.config(function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    "self",
    /(wav)$/,
  ]);
})
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

    $scope.updateItems = function(result){
        $scope.filteredItems = _.filter($scope.items, function(item){
            return item.correct == result;
        })
        console.log(0);
    }
});
