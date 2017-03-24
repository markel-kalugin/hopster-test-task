/**
 * Created by markel on 24.03.17.
 */

angular
    .module('app')
    .controller('User.IndexController', Controller);

function Controller(UserService, $location, $rootScope, FlashService, $log) {
    var vm = this;

    UserService.get(function(data) {
        if (data['status'] === 'OK') {
            FlashService.Success('Got a list of users', true);
            vm.persons = data.body;
        } else {
            FlashService.Error(data['error_message']);
        }
    });
}
