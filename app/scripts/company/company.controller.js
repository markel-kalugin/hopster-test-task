/**
 * Created by markel on 26.03.17.
 */

angular
    .module('app')
    .controller('Company.IndexController', Controller);

function Controller(CompanyService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;
    var init = function () {
        CompanyService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.company = data.body;
            } else {
                FlashService.Error(data['error_message']);
            }
        });
    };

    vm.viewRecord = function (id) {
        if (id > 0) {
            CompanyService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/company/company.view_record.html',
                        controller: 'Company.ViewRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            }
                        }
                    });
                } else {
                    FlashService.Error(data['error_message']);
                }
            });
        }
    };

    vm.addRecord = function () {
        modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'views/company/company.add_record.html',
            controller: 'Company.AddRecordController',
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
            CompanyService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/company/company.edit_record.html',
                        controller: 'Company.EditRecordController',
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
                } else {
                    FlashService.Error(data['error_message']);
                }
            });
        }
    };

    vm.deleteRecord = function (id) {
        if (confirm('Are you sure you want to delete this?')) {
            CompanyService.remove({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    init();
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
    .controller('Company.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, $uibModalStack) {
    function init() {
        $scope.company = record;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('Company.AddRecordController', AddRecordController);

function AddRecordController(CompanyService, FlashService, $scope, $http, getEntityList, $uibModalStack) {
    $scope.saveCompany = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.name) || $scope.name === '') {
            alert('Company name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.description) || $scope.description === '') {
            alert('Company description is empty');
            return;
        } else {
            $scope.datas.name = $scope.name;
            $scope.datas.description = $scope.description;
        }
        CompanyService.create($scope.datas, function (data) {
            if (data['status'] === 'OK') {
                getEntityList();
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
    .controller('Company.EditRecordController', EditRecordController);

function EditRecordController(CompanyService, FlashService, $scope, $http, record, getEntityList, $uibModalStack) {
    $scope.company = {};
    function init() {
        $scope.company.id = record.id;
        $scope.company.name = record.name;
        $scope.company.description = record.description;
    }

    $scope.updateCompany = function () {
        if (!angular.isDefined($scope.company.name) || $scope.company.name === '') {
            alert('Company name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.company.description) || $scope.company.description === '') {
            alert('Company description is empty');
            return;
        }
        CompanyService.update($scope.company, function (data) {
            if (data['status'] === 'OK') {
                getEntityList();
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

