/**
 * Created by markel on 24.03.17.
 */

angular
    .module('app')
    .controller('User.IndexController', Controller);

function Controller(AuthenticationService, UserService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;
    var init = function () {
        UserService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.persons = data.body;
            } else if (data['status'] === 'error' ||
                data['error_message'] === 'Authentication required' ||
                data['status_code'] === '403') {
                AuthenticationService.Logout();
                FlashService.Error(data['error_message']);
            } else {
                FlashService.Error(data['error_message']);
            }
        });
    };

    vm.viewRecord = function (id) {
        if (id > 0) {
            UserService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    FlashService.Success('Got of user', true);
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/user/user.view_record.html',
                        controller: 'User.ViewRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            }
                        }
                    });
                } else if (data['status'] === 'error' ||
                    data['error_message'] === 'Authentication required' ||
                    data['status_code'] === '403') {
                    AuthenticationService.Logout();
                    FlashService.Error(data['error_message']);
                } else {
                    FlashService.Error(data['error_message']);
                }
            });
        }
    };

    vm.addRecord = function () {
        modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'views/user/user.add_record.html',
            controller: 'User.AddRecordController',
            scope: $scope,
            size: '',
            resolve: {
                getEntityList: function () {
                    return init;
                }
            }
        });
    };

    vm.editRecord = function (id) {
        if (id > 0) {
            UserService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    FlashService.Success('Got of user', true);
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/user/user.edit_record.html',
                        controller: 'User.EditRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            getEntityList: function () {
                                return init;
                            }
                        }
                    });
                } else if (data['status'] === 'error' ||
                    data['error_message'] === 'Authentication required' ||
                    data['status_code'] === '403') {
                    AuthenticationService.Logout();
                    FlashService.Error(data['error_message']);
                } else {
                    FlashService.Error(data['error_message']);
                }
            });
        }
    };

    vm.deleteRecord = function (id) {
        if (confirm('Are you sure you want to delete this?')) {
            UserService.remove({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    FlashService.Success('Got a list of users', true);
                    init();
                } else if (data['status'] === 'error' ||
                    data['error_message'] === 'Authentication required' ||
                    data['status_code'] === '403') {
                    AuthenticationService.Logout();
                    FlashService.Error(data['error_message']);
                } else {
                    FlashService.Error(data['error_message']);
                }
            });
        }
    };

    init();

}


angular
    .module('app')
    .controller('User.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, $uibModalStack) {
    function init() {
        $scope.person = record;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('User.AddRecordController', AddRecordController);

function AddRecordController(UserService, FlashService, $scope, $http, getEntityList, $uibModalStack) {
    $scope.savePerson = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.firstname) || $scope.firstname === '') {
            alert('Person firstname is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.lastname) || $scope.lastname === '') {
            alert('Person lastname is empty');
            return;
        } else if (
            !angular.isDefined($scope.username) || $scope.username === '') {
            alert('Person username is empty');
            return;
        } else if (
            !angular.isDefined($scope.email) || $scope.email === '') {
            alert('Person email is empty');
            return;
        } else if (
            !angular.isDefined($scope.password) || $scope.password === '') {
            alert('Person password is empty');
            return;
        } else {
            $scope.datas.firstname = $scope.firstname;
            $scope.datas.lastname = $scope.lastname;
            $scope.datas.username = $scope.username;
            $scope.datas.email = $scope.email;
            $scope.datas.password = $scope.password;
        }
        UserService.create($scope.datas, function (data) {
            if (data['status'] === 'OK') {
                FlashService.Success('User successfully created', true);
                getEntityList();
            } else if (data['status'] === 'error' ||
                data['error_message'] === 'Authentication required' ||
                data['status_code'] === '403') {
                AuthenticationService.Logout();
                FlashService.Error(data['error_message']);
            } else {
                FlashService.Error(data['error_message']);
            }
        });
        $uibModalStack.dismissAll();
    };

    $scope.closeModal = function () {
        getEntityList();
        $uibModalStack.dismissAll();
    };

};


angular
    .module('app')
    .controller('User.EditRecordController', EditRecordController);

function EditRecordController(UserService, FlashService, $scope, $http, record, getEntityList, $uibModalStack) {
    $scope.person = {};
    function init() {
        $scope.person.id = record.id;
        $scope.person.firstname = record.firstname;
        $scope.person.lastname = record.lastname;
        $scope.person.username = record.username;
        $scope.person.email = record.email;
        $scope.person.password = '';
    }

    $scope.updatePerson = function () {
        if (!angular.isDefined($scope.person.firstname) || $scope.person.firstname === '') {
            alert('Person firstname is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.person.lastname) || $scope.person.lastname === '') {
            alert('Person lastname is empty');
            return;
        } else if (
            !angular.isDefined($scope.person.username) || $scope.person.username === '') {
            alert('Person username is empty');
            return;
        } else if (
            !angular.isDefined($scope.person.email) || $scope.person.email === '') {
            alert('Person email is empty');
            return;
        } else if (
            !angular.isDefined($scope.person.password) || $scope.person.password === '') {
            alert('Person password is empty');
            return;
        }
        UserService.update($scope.person, function (data) {
            if (data['status'] === 'OK') {
                FlashService.Success('User successfully updated', true);
                getEntityList();
            } else if (data['status'] === 'error' ||
                data['error_message'] === 'Authentication required' ||
                data['status_code'] === '403') {
                AuthenticationService.Logout();
                FlashService.Error(data['error_message']);
            } else {
                FlashService.Error(data['error_message']);
            }
        });
        $uibModalStack.dismissAll();
    };

    $scope.closeModal = function () {
        getEntityList();
        $uibModalStack.dismissAll();
    };

    init();
};

