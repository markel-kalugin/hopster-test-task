/**
 * Created by markel on 26.03.17.
 */

angular
    .module('app')
    .controller('Manufacturer.IndexController', Controller);

function Controller(AuthenticationService, ProductService, PhoneNumberTypeService, ManufacturerService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;

    ProductService.get(function (data) {
        if (data['status'] === 'OK') {
            vm.products = data.body;
        } else if (data['status'] === 'error' ||
            data['error_message'] === 'Authentication required' ||
            data['status_code'] === '403') {
            AuthenticationService.Logout();
            FlashService.Error(data['error_message']);
        } else {
            FlashService.Error(data['error_message']);
        }
    });

    PhoneNumberTypeService.get(function (data) {
        if (data['status'] === 'OK') {
            vm.phone_number_types = data.body;
        } else if (data['status'] === 'error' ||
            data['error_message'] === 'Authentication required' ||
            data['status_code'] === '403') {
            AuthenticationService.Logout();
            FlashService.Error(data['error_message']);
        } else {
            FlashService.Error(data['error_message']);
        }
    });

    var init = function () {
        ManufacturerService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.manufacturers = data.body;
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
            ManufacturerService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/manufacturer/manufacturer.view_record.html',
                        controller: 'Manufacturer.ViewRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            productsLisr: function () {
                                return vm.products
                            },
                            phoneNumberTypes: function () {
                                return vm.phone_number_types
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
            templateUrl: 'views/manufacturer/manufacturer.add_record.html',
            controller: 'Manufacturer.AddRecordController',
            scope: $scope,
            size: '',
            resolve: {
                getEntityList: function () {
                    return init;
                },
                productsLisr: function () {
                    return vm.products
                },
                phoneNumberTypes: function () {
                    return vm.phone_number_types
                }
            }
        });
    };

    vm.editRecord = function (id) {
        if (id > 0) {
            ManufacturerService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/manufacturer/manufacturer.edit_record.html',
                        controller: 'Manufacturer.EditRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            getEntityList: function () {
                                return init;
                            },
                            productsLisr: function () {
                                return vm.products
                            },
                            phoneNumberTypes: function () {
                                return vm.phone_number_types
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
            ManufacturerService.remove({id: id}, function (data) {
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
    .controller('Manufacturer.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, $uibModalStack) {
    function init() {
        $scope.manufacturer = record;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('Manufacturer.AddRecordController', AddRecordController);

function AddRecordController(ManufacturerService, FlashService, $scope, $http, getEntityList, productsLisr, phoneNumberTypes, $uibModalStack) {
    $scope.products = productsLisr;
    $scope.phone_number_types = phoneNumberTypes;
    $scope.saveManufacturer = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.details) || $scope.details === '') {
            alert('Manufacturer details is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.products) || $scope.products === '') {
            alert('Manufacturer products is empty');
            return;
        } else if (
            !angular.isDefined($scope.phone_number) || $scope.phone_number === '') {
            alert('Manufacturer phone number is empty');
            return;
        } else if (
            !angular.isDefined($scope.phone_number_type) || $scope.phone_number_type === '') {
            alert('Manufacturer phone number type is empty');
            return;
        } else {
            $scope.datas.details = $scope.details;
            $scope.datas.products_manufacturer = $scope.products_manufacturer;
            $scope.datas.phone_number = $scope.phone_number;
            $scope.datas.phone_number_type = $scope.phone_number_type;
        }
        ManufacturerService.create($scope.datas, function (data) {
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
    .controller('Manufacturer.EditRecordController', EditRecordController);

function EditRecordController(ManufacturerService, FlashService, $scope, $http, record, getEntityList, productsLisr, phoneNumberTypes, $uibModalStack) {
    $scope.manufacturer = {};
    function init() {
        $scope.products = productsLisr;
        $scope.phone_number_types = phoneNumberTypes;
        $scope.manufacturer.id = record.id;
        $scope.manufacturer.details = record.details;
        $scope.manufacturer.products_manufacturer = record.products_manufacturer;
        $scope.manufacturer.phone_number = record.phone_number[0];
        $scope.manufacturer.phone_number_type = record.phone_number_type;
    }

    $scope.updateManufacturer = function () {
        if (!angular.isDefined($scope.manufacturer.details) || $scope.manufacturer.details === '') {
            alert('Manufacturer details is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.manufacturer.products_manufacturer) || $scope.manufacturer.products_manufacturer === '') {
            alert('Manufacturer products is empty');
            return;
        } else if (
            !angular.isDefined($scope.manufacturer.phone_number) || $scope.manufacturer.phone_number === '') {
            alert('Manufacturer phone number is empty');
            return;
        } else if (
            !angular.isDefined($scope.manufacturer.phone_number_type) || $scope.manufacturer.phone_number_type === '') {
            alert('Manufacturer phone number type is empty');
            return;
        }
        ManufacturerService.update($scope.manufacturer, function (data) {
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

