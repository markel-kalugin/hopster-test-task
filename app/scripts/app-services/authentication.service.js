/**
 * Created by markel on 12.03.17.
 */
angular
    .module('app')
    .factory('AuthenticationService', Service);

function Service($http, $localStorage) {
    var service = {};

    service.Login = Login;
    service.Logout = Logout;

    return service;

    function Login(username, password, callback) {
        $http.post('/api/v1/authenticate', { username: username, password: password })
            .success(function (response) {
                if (response.body) {
                    $localStorage.currentUser = { username: username, token: response.body };
                    $http.defaults.headers.common.Authorization = 'Bearer ' + response.body;
                    callback(true);
                } else {
                    callback(false);
                }
            });
    }

    function Logout() {
        delete $localStorage.currentUser;
        $http.defaults.headers.common.Authorization = '';
    }
}