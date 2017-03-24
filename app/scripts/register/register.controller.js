/**
 * Created by markel on 12.03.17.
 */
angular
    .module('app')
    .controller('Register.IndexController', Controller);

function Controller(UserService, $location, $rootScope, FlashService, $log) {
    var vm = this;


    vm.createUser = function() {
        vm.dataLoading = true;
        UserService.create(vm.user, function(data) {
            if (data['status'] === 'OK') {
                FlashService.Success('Registration successful', true);
                $location.path('/login');
            } else {
                FlashService.Error(data['error_message']);
                vm.dataLoading = false;
            }
        });
    };

    // Get a user
    vm.getUser = function() {
        UserService.get({username: vm.user.username}, function(data) {
           // do something which you want with response
        });
    };

    // Update a user
    vm.updateUser = function() {
        UserService.update(vm.user, function(data) {
            // do something which you want with response
       });
    };

    // Delete a user
    vm.deleteUser = function() {
        UserService.remove({username: vm.user.username}, function(data) {
         // do something which you want with response
        });
    };
}