/**
 * Created by markel on 26.03.17.
 */
angular.module('app')
.factory('CompanyBrandService', Service);

function Service($resource) {
    return $resource('https://hopstertest-161207.appspot.com/api/v1/company_brand', {}, {
        query: { method: "GET", isArray: false },
        create: { method: "POST"},
        get: { method: "GET"},
        remove: { method: "DELETE"},
        update: { method: "PUT"}
    });
}