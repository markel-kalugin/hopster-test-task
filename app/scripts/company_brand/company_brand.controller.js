/**
 * Created by markel on 26.03.17.
 */

angular
    .module('app')
    .controller('CompanyBrand.IndexController', Controller);

function Controller(AuthenticationService, CompanyService, CompanyBrandService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;

    CompanyService.get(function (data) {
        if (data['status'] === 'OK') {
            vm.companies = data.body;
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
        CompanyBrandService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.company_brands = data.body;
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
            CompanyBrandService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/company_brand/company_brand.view_record.html',
                        controller: 'CompanyBrand.ViewRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            companiesList: function () {
                                return vm.companies;
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
            templateUrl: 'views/company_brand/company_brand.add_record.html',
            controller: 'CompanyBrand.AddRecordController',
            scope: $scope,
            size: '',
            resolve: {
                getEntityList: function () {
                    return init;
                },
                companiesList: function () {
                    return vm.companies;
                }
            }
        });
    };

    vm.editRecord = function (id) {
        if (id > 0) {
            CompanyBrandService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/company_brand/company_brand.edit_record.html',
                        controller: 'CompanyBrand.EditRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            getEntityList: function () {
                                return init;
                            },
                            companiesList: function () {
                                return vm.companies;
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
            CompanyBrandService.remove({id: id}, function (data) {
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
    .controller('CompanyBrand.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, companiesList, $uibModalStack) {
    function init() {
        $scope.company_brand = record;
        $scope.companies = companiesList;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('CompanyBrand.AddRecordController', AddRecordController);

function AddRecordController(CompanyBrandService, FlashService, $scope, $http, getEntityList, companiesList, $uibModalStack, $log) {
    $scope.companies = companiesList;
    $scope.saveCompanyBrand = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.name) || $scope.name === '') {
            alert('Brand name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.company) || $scope.company === '') {
            alert('Brand company is empty');
            return;
        } else {
            $scope.datas.name = $scope.name;
            $scope.datas.company = $scope.company;
        }
        CompanyBrandService.create($scope.datas, function (data) {
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
    .controller('CompanyBrand.EditRecordController', EditRecordController);

function EditRecordController(CompanyBrandService, FlashService, $scope, $http, record, getEntityList, companiesList, $uibModalStack) {
    $scope.company_brand = {};
    function init() {
        $scope.companies = companiesList;
        $scope.company_brand.id = record.id;
        $scope.company_brand.name = record.name;
        $scope.company_brand.company = record.company;
    }

    $scope.updateCompanyBrand = function () {
        if (!angular.isDefined($scope.company_brand.name) || $scope.company_brand.name === '') {
            alert('Brand name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.company_brand.company) || $scope.company_brand.company === '') {
            alert('Brand company is empty');
            return;
        }
        CompanyBrandService.update($scope.company_brand, function (data) {
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
