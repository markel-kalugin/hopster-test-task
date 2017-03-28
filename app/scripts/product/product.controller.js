/**
 * Created by markel on 26.03.17.
 */

angular
    .module('app')
    .controller('Product.IndexController', Controller);

function Controller(ProductCategoryService, CompanyBrandService, ProductService, $location, $scope, $rootScope, FlashService, $uibModal, $log) {
    var vm = this;
    var modalInstance = null;

    ProductCategoryService.get(function (data) {
        if (data['status'] === 'OK') {
            vm.product_categories = data.body;
        } else {
            FlashService.Error(data['error_message']);
        }
    });

    CompanyBrandService.get(function (data) {
        if (data['status'] === 'OK') {
            vm.company_brands = data.body;
        } else {
            FlashService.Error(data['error_message']);
        }
    });

    var init = function () {
        ProductService.get(function (data) {
            if (data['status'] === 'OK') {
                vm.products = data.body;
            } else {
                FlashService.Error(data['error_message']);
            }
        });
    };

    vm.viewRecord = function (id) {
        if (id > 0) {
            ProductService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/product/product.view_record.html',
                        controller: 'Product.ViewRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            companyBrandsList: function () {
                                return vm.company_brands;
                            },
                            productCategoriesList: function () {
                                return vm.product_categories;
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
            templateUrl: 'views/product/product.add_record.html',
            controller: 'Product.AddRecordController',
            scope: $scope,
            size: '',
            resolve: {
                getEntityList: function () {
                    return init;
                },
                companyBrandsList: function () {
                    return vm.company_brands;
                },
                productCategoriesList: function () {
                    return vm.product_categories;
                }
            }
        });
    };

    vm.editRecord = function (id) {
        if (id > 0) {
            ProductService.get({id: id}, function (data) {
                if (data['status'] === 'OK') {
                    modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'views/product/product.edit_record.html',
                        controller: 'Product.EditRecordController',
                        scope: $scope,
                        size: '',
                        resolve: {
                            record: function () {
                                return data.body;
                            },
                            getEntityList: function () {
                                return init;
                            },
                            companyBrandsList: function () {
                                return vm.company_brands;
                            },
                            productCategoriesList: function () {
                                return vm.product_categories;
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
            ProductService.remove({id: id}, function (data) {
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
    .controller('Product.ViewRecordController', ViewRecordController);

function ViewRecordController($scope, $http, record, $uibModalStack) {
    function init() {
        $scope.product = record;
    }

    $scope.closeModal = function () {
        $uibModalStack.dismissAll();
    };

    init();
}


angular
    .module('app')
    .controller('Product.AddRecordController', AddRecordController);

function AddRecordController(ProductService, FlashService, $scope, $http, getEntityList, companyBrandsList, productCategoriesList, $uibModalStack) {
    $scope.company_brands = companyBrandsList;
    $scope.product_categories = productCategoriesList;
    $scope.saveProduct = function () {
        $scope.datas = {};

        if (!angular.isDefined($scope.price) || $scope.price === '') {
            alert('Product price is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.description) || $scope.description === '') {
            alert('Product description is empty');
            return;
        } else if (
            !angular.isDefined($scope.company_brand) || $scope.company_brand === '') {
            alert('Product brand is empty');
            return;
        } else if (
            !angular.isDefined($scope.product_category) || $scope.product_category === '') {
            alert('Product category is empty');
            return;
        } else {
            $scope.datas.price = $scope.price;
            $scope.datas.description = $scope.description;
            $scope.datas.company_brand = $scope.company_brand;
            $scope.datas.product_category = $scope.product_category;
        }
        ProductService.create($scope.datas, function (data) {
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
    .controller('Product.EditRecordController', EditRecordController);

function EditRecordController(ProductService, FlashService, $scope, $http, record, getEntityList, companyBrandsList, productCategoriesList, $uibModalStack) {
    $scope.product = {};
    function init() {
        $scope.company_brands = companyBrandsList;
        $scope.product_categories = productCategoriesList;
        $scope.product.id = record.id;
        $scope.product.price = record.price;
        $scope.product.description = record.description;
        $scope.product.company_brand = record.company_brand;
        $scope.product.product_category = record.product_category;
    }

    $scope.updateProduct = function () {
        if (!angular.isDefined($scope.product.price) || $scope.product.price === '') {
            alert('Product price is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.product.price) || !angular.isNumber($scope.product.price)) {
            alert('Product price must be an integer');
            return;
        }
        else if (
            !angular.isDefined($scope.product.description) || $scope.product.description === '') {
            alert('Product description is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.product.company_brand) || $scope.product.company_brand === '') {
            alert('Product brand is empty');
            return;
        }
        else if (
            !angular.isDefined($scope.product.product_category) || $scope.product.product_category === '') {
            alert('Product category is empty');
            return;
        }
        ProductService.update($scope.product, function (data) {
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

