var app = angular.module('garage-warden', ['ngRoute', 'ui.bootstrap']);
app.controller('mainController', ['$scope','$http','$interval', '$timeout', function($scope, $http, $interval, $timeout){
    $scope.garageFullOpen = null;
    $scope.garageFullClose = null;
    $scope.garageStatus = "unknown";
    $scope.showOperating=true;
    $scope.activateButtonText="Activate Garage";
    $scope.error = null;
    $scope.warning = null;
    $scope.stopStatusMonitor = undefined;

    function monitorStatus(time){
        $scope.stopStatusMonitor = $interval($scope.updateStatus, time);
    }

    function stopMonitorStatus(){
        if(angular.isDefined($scope.stopStatusMonitor)){
            $interval.cancel($scope.stopStatusMonitor);
            $scope.stopStatusMonitor=undefined;
        }
    }

    $scope.updateStatus = function(){
        if($scope.user.loggedIn) {
            $http.get("/api/garage/status").then(function (response) {
                $scope.garageFullClose = response.data.garageFullClose;
                $scope.garageFullOpen = response.data.garageFullOpen;
                stopMonitorStatus();
                if ($scope.garageFullClose) {
                    $scope.garageStatus = "closed";
                    $scope.activateButtonText = "Open Garage";
                    monitorStatus(3000);
                } else if ($scope.garageFullOpen) {
                    $scope.garageStatus = "open";
                    $scope.activateButtonText = "Close Garage";
                    monitorStatus(3000);
                } else {
                    $scope.garageStatus = "operating";
                    $scope.activateButtonText = "Activate Garage";
                    monitorStatus(500);
                }

            });
        }
    };

    $scope.activateGarage = function(){
        $scope.warning=null;
        $scope.error=null;
        $http.post("/api/garage/control", {open: $scope.garageFullClose ? true : false}).then(function(response){
            if(response.data.changed === true){
                $timeout($scope.updateStatus, 1000);
            } else {
                $scope.warning = "Garage state not changed. It was either already in the state requested or currently operating.";
            }
        }, function(response){
            $scope.error=response.data;
        });
    };

    $scope.$watch('user', function(newUser){
        if(newUser && newUser.loggedIn){
            $scope.updateStatus();
        }
    }, true);


    var stopOperatingBlink = $interval(function(){
        $scope.showOperating = !$scope.showOperating;
    }, 400);
    $scope.destroy = function(){
        stopMonitorStatus();
        if(angular.isDefined(stopOperatingBlink)){
            $interval.cancel(stopOperatingBlink);
            stopOperatingBlink = undefined;
        }
    };

    $scope.$on('$destroy', function(){
        $scope.destroy();
    });

    $scope.updateStatus();
}]);
app.controller('loginController', ['$scope', '$http', '$location',
    function ($scope, $http, $location) {
    if($scope.user.loggedIn){
        $location.path("/");
    }
    $scope.$watch('user', function(newUser){
        if(newUser && newUser.loggedIn){
            $location.path("/");
        }
    }, true);

    $scope.error = null;
    $scope.submit = function(){
        $http.post("/api/login", {username:$scope.username, password: $scope.password}).then(
            function (response) {
                angular.copy(response.data, $scope.$root.user);
            }, function(response){
                $scope.error = response.data;
            }
        )
    }
}]);
app.directive('settingForm', [function(){
    return {
        templateUrl: "templates/setting_form.html"
    }
}]);
app.controller('settingsController', ['$scope', '$http', function($scope, $http){
    $scope.settings = null;
    $scope.failed = false;
    $scope.error = null;
    $scope.dirty = {};
    $http.get("/api/settings").then(function(response){
        var settings = {};
        angular.forEach(response.data.settings, function(value){
            var split = value.key.split(".");
            var group = split.shift();
            var name = split.join(".");
            if( !settings[group] ){
                settings[group] = [];
            }
            value.name = name;
            settings[group].push(value);
        });
        $scope.settings = settings;
    });

    $scope.$on('$locationChangeStart', function(event){
        if(Object.keys($scope.dirty).length != 0){
            if(!confirm("You have unsaved changes, are you sure you want to proceed?")){
                event.preventDefault();
            }
        }
    });

    $scope.markDirty = function (setting) {
        $scope.dirty[setting.key] = setting;
    };

    $scope.save = function(){
        if(Object.keys($scope.dirty).length == 0){
            alert("No changes to save!");
            return;
        }
        var settings = [];
        angular.forEach($scope.dirty, function(value){
            settings.push(value);
        });
        $http.post("/api/settings", settings).then(function(){
            $scope.dirty = {};
            $scope.toggleSettings();
        }, function(response){
            $scope.failed=true;
            $scope.error = response.data;
        });
    }
}]);
app.factory("authInterceptor", ["$location","$q","$rootScope", function($location, $q, $rootScope){
    return {
        "responseError": function (response) {
            if(response.status === 401){
                $rootScope.user.loggedIn=false;
                $rootScope.user.name=null;
                $location.path("/login");
            }
            return $q.reject(response);
        }
    }
}]);

app.config(['$routeProvider','$httpProvider',function($routeProvider, $httpProvider){
    $routeProvider
        .when("/", {
            templateUrl : "templates/main.html",
            controller: 'mainController'
        })
        .when("/login", {
            templateUrl : "templates/login.html",
            controller: "loginController"
        })
        .when("/settings", {
            templateUrl : "templates/settings.html",
            controller: "settingsController"
        });
    $httpProvider.interceptors.push('authInterceptor')
}]);
app.run(['$http', '$location', '$rootScope', function($http, $location, $rootScope){
    $rootScope.user = {loggedIn:false};
    $rootScope.logout = function(){
        $http.get("/api/logout").then(function(){
            $rootScope.user.loggedIn=false;
            $rootScope.user.name=null;
            $location.path("/login")
        });
    };
    $rootScope.currentPath = function(){return $location.path()};
    $rootScope.lastPath = $location.path();
    $rootScope.toggleSettings = function(){
        if($location.path() == "/settings"){
            if($rootScope.lastPath == "/settings"){
                $location.path("/");
            } else {
                $location.path($rootScope.lastPath);
            }
        } else {
            $rootScope.lastPath = $location.path();
            $location.path("/settings");
        }
    };
    $http.get("/api/login").then(function(response){
        $rootScope.user.loggedIn = response.data.loggedIn;
        $rootScope.user.name = response.data.name;
        if(!$rootScope.user.loggedIn){
            $location.path("/login");
        }
    });
}]);