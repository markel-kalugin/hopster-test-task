from google.appengine.ext import db


class PersonModel(db.Model):
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    username = db.StringProperty()
    email = db.StringProperty()
    password = db.StringProperty()


class RefProductCategoriesModel(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()


class CompanyModel(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()


class CompanyBrandsModel(db.Model):
    company = db.ReferenceProperty(
        CompanyModel,
        required=True,
        collection_name='company_brand'
    )
    name = db.StringProperty()


class ProductModel(db.Model):
    brand = db.ReferenceProperty(
        CompanyBrandsModel,
        required=True,
        collection_name='brand'
    )
    category = db.ReferenceProperty(
        RefProductCategoriesModel,
        required=True,
        collection_name='product_category'
    )
    price = db.IntegerProperty()
    description = db.StringProperty()


class ManufacturerModel(db.Model):
    details = db.StringProperty()


class ProductManufacturersModel(db.Model):
    product = db.ReferenceProperty(ProductModel, collection_name='manufacturers')
    manufacturer = db.ReferenceProperty(ManufacturerModel, collection_name='products')


class RefPhoneNumbersTypesModel(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()


class PhoneNumbersModel(db.Model):
    manufacturer = db.ReferenceProperty(
        ManufacturerModel,
        required=True,
        collection_name='manufacturer_phone'
    )
    type = db.ReferenceProperty(
        RefPhoneNumbersTypesModel,
        required=True,
        collection_name='phone_type'
    )
    phone = db.StringProperty()
