/**
 * Created by markel on 26.03.17.
 */

angular
    .module('app')
    .controller('PhoneNumbersType.IndexController', Controller);

function Controller(AuthenticationService, PhoneNumberTypeService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;
    var init = function () {
        PhoneNumberTypeService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.phone_number_type = data.body;
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
            PhoneNumberTypeService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/phone_number_type/phone_number_type.view_record.html',
                        controller: 'PhoneNumbersType.ViewRecordController',
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
            templateUrl: 'views/phone_number_type/phone_number_type.add_record.html',
            controller: 'PhoneNumbersType.AddRecordController',
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
            PhoneNumberTypeService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/phone_number_type/phone_number_type.edit_record.html',
                        controller: 'PhoneNumbersType.EditRecordController',
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
            PhoneNumberTypeService.remove({id: id}, function (data) {
                if (data['status'] === 'OK') {
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
    .controller('PhoneNumbersType.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, $uibModalStack) {
    function init() {
        $scope.phone_number_type = record;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('PhoneNumbersType.AddRecordController', AddRecordController);

function AddRecordController(PhoneNumberTypeService, FlashService, $scope, $http, getEntityList, $uibModalStack) {
    $scope.savePhoneNumbersType = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.name) || $scope.name === '') {
            alert('Phone number type name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.description) || $scope.description === '') {
            alert('Phone number type description is empty');
            return;
        } else {
            $scope.datas.name = $scope.name;
            $scope.datas.description = $scope.description;
        }
        PhoneNumberTypeService.create($scope.datas, function (data) {
            if (data['status'] === 'OK') {
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
    .controller('PhoneNumbersType.EditRecordController', EditRecordController);

function EditRecordController(PhoneNumberTypeService, FlashService, $scope, $http, record, getEntityList, $uibModalStack) {
    $scope.phone_number_type = {};
    function init() {
        $scope.phone_number_type.id = record.id;
        $scope.phone_number_type.name = record.name;
        $scope.phone_number_type.description = record.description;
    }

    $scope.updatePhoneNumbersType = function () {
        if (!angular.isDefined($scope.phone_number_type.name) || $scope.phone_number_type.name === '') {
            alert('Phone number type name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.phone_number_type.description) || $scope.phone_number_type.description === '') {
            alert('Phone number type description is empty');
            return;
        }
        PhoneNumberTypeService.update($scope.phone_number_type, function (data) {
            if (data['status'] === 'OK') {
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

