import hashlib

from model import *


class Person(object):
    def save_person(self, firstname, lastname, username, email, password):
        person = PersonModel()
        person.firstname = firstname
        person.lastname = lastname
        person.username = username
        person.email = email
        person.password = self.encrypt_password(password)
        person.put()

    def update_person(self, firstname, lastname, username, email, password, id):
        person = PersonModel.get_by_id(long(id))
        person.firstname = firstname
        person.lastname = lastname
        person.username = username
        person.email = email
        person.password = self.encrypt_password(password)
        person.put()

    def delete_person(self, id):
        if id > 0:
            person_key = db.Key.from_path('PersonModel', long(id))
            db.delete(person_key)
            return True
        else:
            return False

    def get_person_by_id(self, id):
        person = PersonModel.get_by_id(long(id))
        result = {
            'id': person.key().id_or_name(),
            'firstname': person.firstname,
            'lastname': person.lastname,
            'username': person.username,
            'email': person.email,
        }
        return result

    def list_person(self):
        result = []
        persons = PersonModel.all()
        for person in persons:
            result.append(
                {
                    'id': person.key().id_or_name(),
                    'firstname': person.firstname,
                    'lastname': person.lastname,
                    'username': person.username,
                    'email': person.email,
                }
            )
        return result

    def auth_list_person(self):
        result = []
        person = PersonModel.all()
        for i in person:
            result.append([i.username, i.password])
        return result

    def encrypt_password(self, password):
        return hashlib.sha512(password).hexdigest()


class Company(object):
    def save_company(self, name, description):
        company = CompanyModel()
        company.name = name
        company.description = description
        company.put()

    def update_company(self, name, description, id):
        company = CompanyModel().get_by_id(long(id))
        company.name = name
        company.description = description
        company.put()

    def delete_company(self, id):
        if id > 0:
            company_key = db.Key.from_path('CompanyModel', long(id))
            db.delete(company_key)
            return True
        else:
            return False

    def get_company_by_id(self, id):
        company = CompanyModel.get_by_id(long(id))
        result = {
            'id': company.key().id_or_name(),
            'name': company.name,
            'description': company.description,
            'brands': [brand.name for brand in CompanyBrandsModel.all().filter('company = ', company.key())]
        }
        return result

    def list_company(self):
        result = []
        companies = CompanyModel.all()
        for company in companies:
            result.append(
                {
                    'id': company.key().id_or_name(),
                    'name': company.name,
                    'description': company.description,
                }
            )
        return result


class CompanyBrands(object):
    def save_company_brand(self, name, company):
        company_brand = CompanyBrandsModel(
            company=CompanyModel.get_by_id(long(company['id']))
        )
        company_brand.name = name
        company_brand.put()

    def update_company_brand(self, name, company, id):
        company_brand = CompanyBrandsModel.get_by_id(long(id))
        company_brand.company = CompanyModel.get_by_id(long(company['id']))
        company_brand.name = name
        company_brand.put()

    def delete_company_brand(self, id):
        if id > 0:
            company_brand_key = db.Key.from_path('CompanyBrandsModel', long(id))
            db.delete(company_brand_key)
            return True
        else:
            return False

    def get_company_brand_by_id(self, id):
        company_brand = CompanyBrandsModel.get_by_id(long(id))
        result = {
            'id': company_brand.key().id_or_name(),
            'name': company_brand.name,
            'company': company_brand.company.name,
        }
        return result

    def list_company_brand(self):
        result = []
        company_brands = CompanyBrandsModel.all()
        for company_brand in company_brands:
            result.append(
                {
                    'id': company_brand.key().id_or_name(),
                    'name': company_brand.name,
                    'company': company_brand.company.name,
                }
            )
        import logging
        logging.info('{}'.format(result))
        return result


class ProductCategory(object):
    def save_product_category(self, name, description):
        product_category = RefProductCategoriesModel()
        product_category.name = name
        product_category.description = description
        product_category.put()

    def update_product_category(self, name, description, id):
        product_category = RefProductCategoriesModel().get_by_id(long(id))
        product_category.name = name
        product_category.description = description
        product_category.put()

    def delete_product_category(self, id):
        if id > 0:
            product_category_key = db.Key.from_path('RefProductCategoriesModel', long(id))
            db.delete(product_category_key)
            return True
        else:
            return False

    def get_product_category_by_id(self, id):
        product_category = RefProductCategoriesModel.get_by_id(long(id))
        result = {
            'id': product_category.key().id_or_name(),
            'name': product_category.name,
            'description': product_category.description,
            'products': [brand.name for brand in
                         ProductModel.all().filter('product_category = ', product_category.key())]
        }
        return result

    def list_product_category(self):
        result = []
        product_categories = RefProductCategoriesModel.all()
        for product_category in product_categories:
            result.append(
                {
                    'id': product_category.key().id_or_name(),
                    'name': product_category.name,
                    'description': product_category.description,
                }
            )
        return result


class Product(object):
    def save_product(self, price, description, company_brand, product_category):
        product = ProductModel(
            brand=CompanyBrandsModel.get_by_id(long(company_brand['id'])),
            category=RefProductCategoriesModel.get_by_id(long(product_category['id']))
        )
        product.price = price
        product.description = description
        product.put()

    def update_product(self, price, description, company_brand, product_category, id):
        product = ProductModel.get_by_id(long(id))
        product.brand = CompanyBrandsModel.get_by_id(long(company_brand['id']))
        product.category = RefProductCategoriesModel.get_by_id(long(product_category['id']))
        product.price = price
        product.description = description
        product.put()

    def delete_product(self, id):
        if id > 0:
            product_key = db.Key.from_path('ProductModel', long(id))
            db.delete(product_key)
            return True
        else:
            return False

    def get_product_by_id(self, id):
        product = ProductModel.get_by_id(long(id))
        result = {
            'id': product.key().id_or_name(),
            'price': product.price,
            'description': product.description,
            'category': product.category.name,
            'brand': product.brand.name,
        }
        return result

    def list_product(self):
        result = []
        products = ProductModel.all()
        for product in products:
            result.append(
                {
                    'id': product.key().id_or_name(),
                    'price': product.price,
                    'description': product.description,
                    'category': product.category.name,
                    'brand': product.brand.name,
                }
            )
        return result


class PhoneNumberType(object):
    def save_phone_number_type(self, name, description):
        phone_number_type = RefPhoneNumbersTypesModel()
        phone_number_type.name = name
        phone_number_type.description = description
        phone_number_type.put()

    def update_phone_number_type(self, name, description, id):
        phone_number_type = RefPhoneNumbersTypesModel().get_by_id(long(id))
        phone_number_type.name = name
        phone_number_type.description = description
        phone_number_type.put()

    def delete_phone_number_type(self, id):
        if id > 0:
            phone_number_type_key = db.Key.from_path('RefPhoneNumbersTypesModel', long(id))
            db.delete(phone_number_type_key)
            return True
        else:
            return False

    def get_phone_number_type_by_id(self, id):
        phone_number_type = RefPhoneNumbersTypesModel.get_by_id(long(id))
        result = {
            'id': phone_number_type.key().id_or_name(),
            'name': phone_number_type.name,
            'description': phone_number_type.description,
            'phones': [phone_type.name for phone_type in
                       PhoneNumbersModel.all().filter('phone_type = ', phone_number_type.key())]
        }
        return result

    def list_phone_number_type(self):
        result = []
        companies = RefPhoneNumbersTypesModel.all()
        for phone_number_type in companies:
            result.append(
                {
                    'id': phone_number_type.key().id_or_name(),
                    'name': phone_number_type.name,
                    'description': phone_number_type.description,
                }
            )
        return result

