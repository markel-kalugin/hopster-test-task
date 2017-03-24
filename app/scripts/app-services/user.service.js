/**
 * Created by markel on 13.03.17.
 */
angular.module('app')
.factory('UserService', Service);

function Service($resource) {
    return $resource('https://hopstertest-161207.appspot.com/api/v1/users', {}, {
        query: { method: "GET", isArray: true },
        create: { method: "POST"},
        get: { method: "GET"},
        remove: { method: "DELETE"},
        update: { method: "PUT"}
    });
}