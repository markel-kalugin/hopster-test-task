/**
 * Created by markel on 26.03.17.
 */
angular.module('app')
.factory('ProductCategoryService', Service);

function Service($resource) {
    return $resource('https://hopstertest-161207.appspot.com/api/v1/product_category', {}, {
        query: { method: "GET", isArray: false },
        create: { method: "POST"},
        get: { method: "GET"},
        remove: { method: "DELETE"},
        update: { method: "PUT"}
    });
}