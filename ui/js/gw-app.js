var app = angular.module('garage-warden', ['ngRoute']);
app.controller('statusController', ['$scope','$http', function($scope,$http){
    $scope.garageFullOpen = null;
    $scope.garageFullClose = null;

    $http.get("http://127.0.0.1:8000/garage/status").then(function(response){
        $scope.garageFullClose = response.data.garageFullClose;
        $scope.garageFullOpen = response.data.garageFullOpen;
    });
}]);
app.config(['$routeProvider', function($routeProvider){
    $routeProvider
        .when("/", {
            redirectTo : "status"
        })
        .when("/status", {
            templateUrl : "templates/status.html",
            controller: 'statusController'
        });
}]);