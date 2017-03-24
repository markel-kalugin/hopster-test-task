/**
 * Created by markel on 12.03.17.
 */
angular
    .module('app', ['ui.router', 'ngMessages', 'ngStorage', 'ngResource'])
    .config(config)
    .run(run);

function config($stateProvider, $urlRouterProvider) {
    // default route
    $urlRouterProvider.otherwise("/");

    // app routes
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: 'views/home/home.view.html',
            controller: 'Home.IndexController',
            controllerAs: 'vm'
        })
        .state('login', {
            url: '/login',
            templateUrl: 'views/login/login.view.html',
            controller: 'Login.IndexController',
            controllerAs: 'vm'
        })
        .state('register', {
            url: '/register',
            templateUrl: 'views/register/register.view.html',
            controller: 'Register.IndexController',
            controllerAs: 'vm'
        }).state('user', {
            url: '/user',
            templateUrl: 'views/user/user.view.html',
            controller: 'User.IndexController',
            controllerAs: 'vm'
        });
}

function run($rootScope, $http, $location, $localStorage) {
    // keep user logged in after page refresh
    if ($localStorage.currentUser) {
        $http.defaults.headers.common.Authorization = 'Bearer ' + $localStorage.currentUser.token;
    }

    // redirect to login page if not logged in and trying to access a restricted page
    $rootScope.$on('$locationChangeStart', function (event, next, current) {
        var restrictedPage = $.inArray($location.path(), ['/login', '/register']) === -1;
        var loggedIn = $localStorage.currentUser;
        if (restrictedPage && !loggedIn) {
            $location.path('/login');
        }
    });
}