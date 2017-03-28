/**
 * Created by markel on 26.03.17.
 */

angular
    .module('app')
    .controller('ProductCategory.IndexController', Controller);

function Controller(ProductCategoryService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;
    
    var init = function () {
        ProductCategoryService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.product_category = data.body;
            } else {
                FlashService.Error(data['error_message']);
            }
        });
    };

    vm.viewRecord = function (id) {
        if (id > 0) {
            ProductCategoryService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/product_category/product_category.view_record.html',
                        controller: 'ProductCategory.ViewRecordController',
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
            templateUrl: 'views/product_category/product_category.add_record.html',
            controller: 'ProductCategory.AddRecordController',
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
            ProductCategoryService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/product_category/product_category.edit_record.html',
                        controller: 'ProductCategory.EditRecordController',
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
            ProductCategoryService.remove({id: id}, function (data) {
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
    .controller('ProductCategory.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, $uibModalStack) {
    function init() {
        $scope.product_category = record;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('ProductCategory.AddRecordController', AddRecordController);

function AddRecordController(ProductCategoryService, FlashService, $scope, $http, getEntityList, $uibModalStack) {
    $scope.saveProductCategory = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.name) || $scope.name === '') {
            alert('ProductCategory name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.description) || $scope.description === '') {
            alert('ProductCategory description is empty');
            return;
        } else {
            $scope.datas.name = $scope.name;
            $scope.datas.description = $scope.description;
        }
        ProductCategoryService.create($scope.datas, function (data) {
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
    .controller('ProductCategory.EditRecordController', EditRecordController);

function EditRecordController(ProductCategoryService, FlashService, $scope, $http, record, getEntityList, $uibModalStack) {
    $scope.product_category = {};
    function init() {
        $scope.product_category.id = record.id;
        $scope.product_category.name = record.name;
        $scope.product_category.description = record.description;
    }

    $scope.updateProductCategory = function () {
        if (!angular.isDefined($scope.product_category.name) || $scope.product_category.name === '') {
            alert('ProductCategory name is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.product_category.description) || $scope.product_category.description === '') {
            alert('ProductCategory description is empty');
            return;
        }
        ProductCategoryService.update($scope.product_category, function (data) {
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

