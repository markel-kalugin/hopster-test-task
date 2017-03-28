import hashlib

from model import *


class Person(object):
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor PersonModel.
    """

    def save(self, firstname, lastname, username, email, password):
        """
        Method for creating new entity instance.

        :param str firstname: User firstname.
        :param str lastname: User lastname.
        :param str username: User username in application it using as login.
        :param str email: User email.
        :param str password: User password.
        :return: None
        :rtype: None
        """
        person = PersonModel()
        person.firstname = firstname
        person.lastname = lastname
        person.username = username
        person.email = email
        person.password = self.encrypt_password(password)
        person.put()

    def update(self, firstname, lastname, username, email, password, id):
        """
        Method for updating entity.

        :param str firstname: User firstname.
        :param str lastname: User lastname.
        :param str username: User username in application it using as login.
        :param str email: User email.
        :param str password: User password.
        :param int id: User id.
        :return: None
        :rtype: None
        """
        person = PersonModel.get_by_id(long(id))
        person.firstname = firstname
        person.lastname = lastname
        person.username = username
        person.email = email
        person.password = self.encrypt_password(password)
        person.put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            person_key = db.Key.from_path('PersonModel', long(id))
            db.delete(person_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        person = PersonModel.get_by_id(long(id))
        result = {
            'id': person.key().id_or_name(),
            'firstname': person.firstname,
            'lastname': person.lastname,
            'username': person.username,
            'email': person.email,
        }
        return result

    def list(self):
        """
        Method for getting list of users with full set of fields but without password.

        :return: List of users fields without password.
        :rtype: list
        """
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
        """
        Method for getting list of users for authentication.

        :return: List of usernames and encrypted passwords
        :rtype: list
        """
        result = []
        person = PersonModel.all()
        for i in person:
            result.append([i.username, i.password])
        return result

    def encrypt_password(self, password):
        """
        Method for encrypting password.

        :param str password: String with password in its pure form.
        :return: Encrypted password
        :rtype: str
        """
        return hashlib.sha512(password).hexdigest()


class Company(object):
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor CompanyModel.
    Also this helper interact with other data model descriptors
    for customizing of business logic, such as:
    1. CompanyBrandsModel
    """

    def save(self, name, description):
        """
        Method for creating new entity instance.

        :param str name: Company name.
        :param str description: Company description.
        :return: None
        :rtype: None
        """
        company = CompanyModel()
        company.name = name
        company.description = description
        company.put()

    def update(self, name, description, id):
        """
        Method for updating entity.

        :param str name: Company name.
        :param str description: Company description.
        :param int id: Company id.
        :return: None
        :rtype: None
        """
        company = CompanyModel().get_by_id(long(id))
        company.name = name
        company.description = description
        company.put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            company_key = db.Key.from_path('CompanyModel', long(id))
            db.delete(company_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        company = CompanyModel.get_by_id(long(id))
        result = {
            'id': company.key().id_or_name(),
            'name': company.name,
            'description': company.description,
            'brands': [brand.name for brand in CompanyBrandsModel.all().filter('company = ', company.key())]
        }
        return result

    def list(self):
        """
        Method for getting list of entity with full set of fields.

        :return: List of entity fields.
        :rtype: list
        """
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
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor CompanyBrandsModel.
    Also this helper interact with other data model descriptors
    for customizing of business logic, such as:
    1. CompanyModel
    """

    def save(self, name, company):
        """
        Method for creating new entity instance.

        :param str name: Brand name.
        :param dict company: Object with company metadata for creating relationship with CompanyModel entity.
        :return: None
        :rtype: None
        """
        company_brand = CompanyBrandsModel(
            company=CompanyModel.get_by_id(long(company['id']))
        )
        company_brand.name = name
        company_brand.put()

    def update(self, name, company, id):
        """
        Method for updating entity.

        :param str name: Brand name.
        :param dict company: Object with company metadata for creating relationship with CompanyModel entity.
        :param int id: Brand id.
        :return: None
        :rtype: None
        """
        company_brand = CompanyBrandsModel.get_by_id(long(id))
        company_brand.company = CompanyModel.get_by_id(long(company['id']))
        company_brand.name = name
        company_brand.put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            company_brand_key = db.Key.from_path('CompanyBrandsModel', long(id))
            db.delete(company_brand_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        company_brand = CompanyBrandsModel.get_by_id(long(id))
        result = {
            'id': company_brand.key().id_or_name(),
            'name': company_brand.name,
            'company': company_brand.company.name,
        }
        return result

    def list(self):
        """
        Method for getting list of entity with full set of fields.

        :return: List of entity fields.
        :rtype: list
        """
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
        return result


class ProductCategory(object):
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor RefProductCategoriesModel.
    Also this helper interact with other data model descriptors
    for customizing of business logic, such as:
    1. ProductModel
    2. RefProductCategoriesModel
    """

    def save(self, name, description):
        """
        Method for creating new entity instance.

        :param str name: Category name.
        :param str description: Category description.
        :return: None
        :rtype: None
        """
        product_category = RefProductCategoriesModel()
        product_category.name = name
        product_category.description = description
        product_category.put()

    def update(self, name, description, id):
        """
        Method for updating entity.

        :param str name: Category name.
        :param str description: Category description.
        :param int id: Category id.
        :return: None
        :rtype: None
        """
        product_category = RefProductCategoriesModel().get_by_id(long(id))
        product_category.name = name
        product_category.description = description
        product_category.put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            product_category_key = db.Key.from_path('RefProductCategoriesModel', long(id))
            db.delete(product_category_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        product_category = RefProductCategoriesModel.get_by_id(long(id))
        result = {
            'id': product_category.key().id_or_name(),
            'name': product_category.name,
            'description': product_category.description,
            'products': [brand.name for brand in
                         ProductModel.all().filter('product_category = ', product_category.key())]
        }
        return result

    def list(self):
        """
        Method for getting list of entity with full set of fields.

        :return: List of entity fields.
        :rtype: list
        """
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
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor ProductModel.
    Also this helper interact with other data model descriptors
    for customizing of business logic, such as:
    1. CompanyBrandsModel
    2. RefProductCategoriesModel
    """

    def save(self, price, description, company_brand, product_category):
        """
        Method for creating new entity instance.

        :param int price: Product price.
        :param str description: Product description.
        :param str company_brand: Object with CompanyBrandsModel instance metadata for creating relationship with ProductModel entity.
        :param str product_category: Object with RefProductCategoriesModel instance metadata for creating relationship with ProductModel entity.
        :return: None
        :rtype: None
        """
        product = ProductModel(
            brand=CompanyBrandsModel.get_by_id(long(company_brand['id'])),
            category=RefProductCategoriesModel.get_by_id(long(product_category['id']))
        )
        product.price = price
        product.description = description
        product.put()

    def update(self, price, description, company_brand, product_category, id):
        """
        Method for updating entity.

        :param int price: Product price.
        :param str description: Product description.
        :param str company_brand: Object with CompanyBrandsModel instance metadata for creating relationship with ProductModel entity.
        :param str product_category: Object with RefProductCategoriesModel instance metadata for creating relationship with ProductModel entity.
        :param int id: Product id.
        :return: None
        :rtype: None
        """
        product = ProductModel.get_by_id(long(id))
        product.brand = CompanyBrandsModel.get_by_id(long(company_brand['id']))
        product.category = RefProductCategoriesModel.get_by_id(long(product_category['id']))
        product.price = price
        product.description = description
        product.put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            product_key = db.Key.from_path('ProductModel', long(id))
            db.delete(product_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        product = ProductModel.get_by_id(long(id))
        result = {
            'id': product.key().id_or_name(),
            'price': product.price,
            'description': product.description,
            'category': product.category.name,
            'brand': product.brand.name,
        }
        return result

    def list(self):
        """
        Method for getting list of entity with full set of fields.

        :return: List of entity fields.
        :rtype: list
        """
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
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor RefPhoneNumbersTypesModel.
    Also this helper interact with other data model descriptors
    for customizing of business logic, such as:
    1. RefPhoneNumbersTypesModel
    """

    def save(self, name, description):
        """
        Method for creating new entity instance.

        :param str name: Phone number name.
        :param str description: Phone number description.
        :return: None
        :rtype: None
        """
        phone_number_type = RefPhoneNumbersTypesModel()
        phone_number_type.name = name
        phone_number_type.description = description
        phone_number_type.put()

    def update(self, name, description, id):
        """
        Method for updating entity.

        :param str name: Phone number name.
        :param str description: Phone number description.
        :param int id: Phone number id.
        :return: None
        :rtype: None
        """
        phone_number_type = RefPhoneNumbersTypesModel().get_by_id(long(id))
        phone_number_type.name = name
        phone_number_type.description = description
        phone_number_type.put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            phone_number_type_key = db.Key.from_path('RefPhoneNumbersTypesModel', long(id))
            db.delete(phone_number_type_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        phone_number_type = RefPhoneNumbersTypesModel.get_by_id(long(id))
        result = {
            'id': phone_number_type.key().id_or_name(),
            'name': phone_number_type.name,
            'description': phone_number_type.description,
            'phones': [
                phone_type.name for phone_type in
                PhoneNumbersModel
                    .all()
                    .filter('phone_type = ', phone_number_type.key())
                ]
        }
        return result

    def list(self):
        """
        Method for getting list of entity with full set of fields.

        :return: List of entity fields.
        :rtype: list
        """
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


class Manufacturer(object):
    """
    Helper for processing CRUD operations with business entity
    which have data model descriptor ManufacturerModel.
    Also this helper interact with other data model descriptors
    for customizing of business logic, such as:
    1. ProductModel
    2. ProductManufacturersModel
    3. PhoneNumbersModel
    4. RefPhoneNumbersTypesModel
    """

    def save(self, details, phone_number, phone_number_type, products_manufacturer):
        """
        Method for creating new entity instance.

        :param str details: Manufacturer details.
        :param str phone_number: Object with PhoneNumbersModel instance metadata for creating relationship with ManufacturerModel entity.
        :param str phone_number_type: Object with RefPhoneNumbersTypesModel instance metadata for creating relationship with ManufacturerModel entity.
        :param str products_manufacturer: Object with ProductModel instance metadata for creating many-to-many relationship with ManufacturerModel entity via intermediate entity ProductManufacturersModel.
        :return: None
        :rtype: None
        """
        manufacturer = ManufacturerModel()
        manufacturer.details = details
        manufacturer.put()

        PhoneNumbersModel(
            manufacturer=manufacturer.key(),
            type=RefPhoneNumbersTypesModel.get_by_id(long(phone_number_type['id'])),
            phone=phone_number
        ).put()

        for _products_manufacturer in products_manufacturer:
            ProductManufacturersModel(
                product=ProductModel.get_by_id(long(_products_manufacturer['id'])),
                manufacturer=manufacturer.key()
            ).put()

    def update(self, details, phone_number, phone_number_type, products_manufacturer, id):
        """
        Method for updating entity.

        :param str details: Manufacturer details.
        :param str phone_number: Object with PhoneNumbersModel instance metadata for creating relationship with ManufacturerModel entity.
        :param str phone_number_type: Object with RefPhoneNumbersTypesModel instance metadata for creating relationship with ManufacturerModel entity.
        :param str products_manufacturer: Object with ProductModel instance metadata for creating many-to-many relationship with ManufacturerModel entity via intermediate entity ProductManufacturersModel.
        :param int id: Manufacturer id.
        :return: None
        :rtype: None
        """
        manufacturer = ManufacturerModel.get_by_id(long(id))
        manufacturer.details = details
        manufacturer.put()

        phone_numbers_keys = [
            _phone_number.key() for _phone_number in
            PhoneNumbersModel
                .all()
                .filter('manufacturer = ', manufacturer.key())
            ]
        db.delete(phone_numbers_keys)

        product_manufacturer_relations_keys = [
            product_manufacturer_relation.key()
            for product_manufacturer_relation in ProductManufacturersModel
                .all()
                .filter('manufacturer =', manufacturer)
            ]
        db.delete(product_manufacturer_relations_keys)

        PhoneNumbersModel(
            manufacturer=manufacturer.key(),
            type=RefPhoneNumbersTypesModel.get_by_id(long(phone_number_type['id'])),
            phone=phone_number
        ).put()

        for _products_manufacturer in products_manufacturer:
            ProductManufacturersModel(
                product=ProductModel.get_by_id(long(_products_manufacturer['id'])),
                manufacturer=manufacturer.key()
            ).put()

    def delete(self, id):
        """
        Method for deleting entity by id.

        :param int id: Entity id.
        :return: Result which means deleted entity or not.
        :rtype: bool
        """
        if id > 0:
            manufacturer_key = db.Key.from_path('ManufacturerModel', long(id))
            db.delete(manufacturer_key)
            return True
        else:
            return False

    def get_by_id(self, id):
        """
        Method for getting entity by id.

        :param int id: Entity id.
        :return: Set of entity parameter.
        :rtype: dict
        """
        manufacturer = ManufacturerModel.get_by_id(long(id))

        phone_numbers = PhoneNumbersModel.all().filter('manufacturer = ', manufacturer.key())

        product_manufacturer_relations_keys = ProductManufacturersModel.all().filter('manufacturer =', manufacturer)
        products_keys = [
            ProductManufacturersModel.product.get_value_for_datastore(relations_key)
            for relations_key in product_manufacturer_relations_keys
            ]
        products = db.get(products_keys)

        result = {
            'id': manufacturer.key().id_or_name(),
            'details': manufacturer.details,
            'phone_number': [phone_number.phone for phone_number in phone_numbers],
            'phone_number_type': [
                {
                    'id': phone_number.type.key().id_or_name(),
                    'name': phone_number.type.name,
                } for phone_number in phone_numbers],
            'products': [
                '{} - {} - {}'.format(
                    product.category.name,
                    product.brand.name,
                    product.price
                ) for product in products
                ],
        }
        return result

    def list(self):
        """
        Method for getting list of entity with full set of fields.

        :return: List of entity fields.
        :rtype: list
        """
        result = []
        manufacturers = ManufacturerModel.all()
        for manufacturer in manufacturers:
            phone_numbers = PhoneNumbersModel.all().filter('manufacturer = ', manufacturer.key())
            result.append(
                {
                    'id': manufacturer.key().id_or_name(),
                    'details': manufacturer.details,
                    'phone_number': [phone_number.phone for phone_number in phone_numbers],
                    'phone_number_type': [
                        {
                            'id': phone_number.type.key().id_or_name(),
                            'name': phone_number.type.name,
                        } for phone_number in phone_numbers],
                }
            )
        return result
