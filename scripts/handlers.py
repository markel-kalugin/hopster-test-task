import logging
import webapp2
from webapp2_extras import sessions
from helpers import (
    Person, Company, CompanyBrands, ProductCategory, Product, PhoneNumberType, Manufacturer
)
import json
import jwt
import time


class BaseHandler(webapp2.RedirectHandler):
    def dispatch(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,OPTIONS,POST,PUT'
        self.response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers,' \
                                                                'Origin,' \
                                                                'Accept,' \
                                                                'X-Requested-With, Content-Type,' \
                                                                'Access-Control-Request-Method,' \
                                                                'Access-Control-Request-Headers'
        self.response.headers['Access-Control-Max-Age'] = '3600'
        self.response.headers['Content-Type'] = 'application/json'

        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            super(BaseHandler, self).dispatch()
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)


    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def response_factory(self, status='OK', body=None, status_code=200, error_message=None):
        self.response.out.write(json.dumps(
                {
                    'status': status,
                    'body': body,
                    'status_code': status_code,
                    'error_message': error_message
                }
            )
        )


class AuthenticationHandler(BaseHandler):
    def post(self):
        params = json.loads(self.request.body)
        person = Person()
        person_list = person.auth_list_person()
        if [params['username'], person.encrypt_password(params['password'])] in person_list:
            token = jwt.encode(
                {
                    'username': params['username'],
                    'timestamp': time.time()
                },
                self.app.config.get('webapp2_extras.sessions')['secret_key'],
                algorithm='HS256'
            )
            logging.info('User with username {} was authenticated'.format(params['username']))
            self.response_factory(
                body=token
            )
        else:
            self.response_factory(
                status='error',
                status_code=407,
                error_message='Person does not exist'
            )


class UserManagementHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Person().get_person_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=Person().list_person()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            person = Person()
            person.save_person(**params)
            logging.info('User with username {} was created.'.format(params['username']))
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            person = Person()
            person.update_person(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Person().delete_person(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class CompanyHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Company().get_company_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=Company().list_company()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            company = Company()
            company.save_company(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            company = Company()
            company.update_company(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Company().delete_company(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class CompanyBrandHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=CompanyBrands().get_company_brand_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=CompanyBrands().list_company_brand()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            company_brand = CompanyBrands()
            company_brand.save_company_brand(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            company_brand = CompanyBrands()
            company_brand.update_company_brand(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=CompanyBrands().delete_company_brand(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class ProductCategoryHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=ProductCategory().get_product_category_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=ProductCategory().list_product_category()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            product_category = ProductCategory()
            product_category.save_product_category(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            product_category = ProductCategory()
            product_category.update_product_category(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=ProductCategory().delete_product_category(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class ProductHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Product().get_product_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=Product().list_product()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            product = Product()
            product.save_product(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            product = Product()
            product.update_product(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Product().delete_product(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class PhoneNumberTypeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=PhoneNumberType().get_phone_number_type_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=PhoneNumberType().list_phone_number_type()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            product = PhoneNumberType()
            product.save_phone_number_type(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            product = PhoneNumberType()
            product.update_phone_number_type(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=PhoneNumberType().delete_phone_number_type(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class ManufacturerHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Manufacturer().get_manufacturer_by_id(self.request.get('id'))
                )
            else:
                self.response_factory(
                    body=Manufacturer().list_manufacturer()
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post(self):
        try:
            params = json.loads(self.request.body)
            product = Manufacturer()
            product.save_manufacturer(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put(self):
        try:
            params = json.loads(self.request.body)
            product = Manufacturer()
            product.update_manufacturer(**params)
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete(self):
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=Manufacturer().delete_manufacturer(self.request.get('id'))
                )
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )
