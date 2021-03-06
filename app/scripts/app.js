/**
 * Created by markel on 12.03.17.
 */
angular
    .module('app', ['ui.router', 'ngMessages', 'ngStorage', 'ngResource', 'smart-table', 'ui.bootstrap',
    'angular-bootstrap-chosen'])
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
        })
        .state('user', {
            url: '/users',
            templateUrl: 'views/user/user.view.html',
            controller: 'User.IndexController',
            controllerAs: 'vm'
        })
        .state('product', {
            url: '/products',
            templateUrl: 'views/product/product.view.html',
            controller: 'Product.IndexController',
            controllerAs: 'vm'
        })
        .state('manufacturer', {
            url: '/manufacturers',
            templateUrl: 'views/manufacturer/manufacturer.view.html',
            controller: 'Manufacturer.IndexController',
            controllerAs: 'vm'
        })
        .state('phone_numbers_type', {
            url: '/phone_number_types',
            templateUrl: 'views/phone_number_type/phone_number_type.view.html',
            controller: 'PhoneNumbersType.IndexController',
            controllerAs: 'vm'
        })
        .state('product_category', {
            url: '/product_categories',
            templateUrl: 'views/product_category/product_category.view.html',
            controller: 'ProductCategory.IndexController',
            controllerAs: 'vm'
        })
        .state('company_brand', {
            url: '/company_brands',
            templateUrl: 'views/company_brand/company_brand.view.html',
            controller: 'CompanyBrand.IndexController',
            controllerAs: 'vm'
        })
        .state('company', {
            url: '/companies',
            templateUrl: 'views/company/company.view.html',
            controller: 'Company.IndexController',
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