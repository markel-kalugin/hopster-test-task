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
    """
    It is necessary to redefine the parameters of responses.
    """

    def dispatch(self):
        """
        Updates header of HTTP packages and stored session.

        :return: None
        :rtype: None
        """
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
        """
        Returns a session using the default cookie key.

        :return: None
        :rtype: None
        """
        return self.session_store.get_session()

    def response_factory(self, status='OK', body=None, status_code=200, error_message=None):
        """
        For unification response body factory.

        :param status: str
        :param body: any
        :param status_code: int
        :param error_message: str
        :return: None
        :rtype: None
        """
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
    """
    Authontication handler
    """

    def post(self):
        """
        Builds token according to current timestamp, secret key and user credentials.

        :return: None
        :rtype: None
        """
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


class CRUDHandler(BaseHandler):
    """
    Due to the identity of the requests handlers logic, all handlers
    are assembled in this class to reduce the lines of code.
    """

    def get_handler(self, class_helper):
        """
        Wrapper for HTTP request handler with method GET was created for upping of abstract level.

        :param class class_helper: is a class which processing some business entity.
        :return: None
        :rtype: None
        """
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=class_helper().get_by_id(self.request.get('id'))
                )
                logging.info('Entity with name {entity_name} was got successfully by id = {id}.'.format(
                    entity_name=class_helper.__name__,
                    id=self.request.get('id')
                ))
            else:
                self.response_factory(
                    body=class_helper().list()
                )
                logging.info('List of entities with name {entity_name} was got successfully.'.format(
                    entity_name=class_helper.__name__
                ))
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def post_handler(self, class_helper):
        """
        Wrapper for HTTP request handler with method POST was created for upping of abstract level.

        :param class class_helper: is a class which processing some business entity.
        :return: None
        :rtype: None
        """
        try:
            params = json.loads(self.request.body)
            entity = class_helper()
            entity.save(**params)
            logging.info('Entity with name {entity_name} was created successfully.'.format(
                entity_name=class_helper.__name__
            ))
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def put_handler(self, class_helper):
        """
        Wrapper for HTTP request handler with method PUT was created for upping of abstract level.

        :param class class_helper: is a class which processing some business entity.
        :return: None
        :rtype: None
        """
        try:
            params = json.loads(self.request.body)
            entity = class_helper()
            entity.update(**params)
            logging.info('Entity with name {entity_name} was updated successfully.'.format(
                entity_name=class_helper.__name__
            ))
            self.response_factory()
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )

    def delete_handler(self, class_helper):
        """
        Wrapper for HTTP request handler with method DELETE was created for upping of abstract level.

        :param class class_helper: is a class which processing some business entity.
        :return: None
        :rtype: None
        """
        try:
            if self.request.get('id'):
                self.response_factory(
                    body=class_helper().delete(self.request.get('id'))
                )
                logging.info('Entity with name {entity_name} was deleted successfully.'.format(
                    entity_name=class_helper.__name__
                ))
        except webapp2.HTTPException as e:
            self.response_factory(
                status='error',
                status_code=407,
                error_message=e.message
            )


class UserManagementHandler(CRUDHandler):
    """
    User Management handler
    """
    helper = Person

    def get(self, *args, **kwargs):
        """
        Handler for request User Management endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request User Management endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request User Management endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request User Management endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)


class CompanyHandler(CRUDHandler):
    """
    Company handler
    """
    helper = Company

    def get(self, *args, **kwargs):
        """
        Handler for request Company endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request Company endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request Company endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request Company endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)


class CompanyBrandHandler(CRUDHandler):
    """
    Company Brands handler
    """
    helper = CompanyBrands

    def get(self, *args, **kwargs):
        """
        Handler for request Company Brands endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request Company Brands endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request Company Brands endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request Company Brands endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)


class ProductCategoryHandler(CRUDHandler):
    """
    Product Category handler
    """
    helper = ProductCategory

    def get(self, *args, **kwargs):
        """
        Handler for request Product Category endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request Product Category endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request Product Category endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request Product Category endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)


class ProductHandler(CRUDHandler):
    """
    Product handler
    """
    helper = Product

    def get(self, *args, **kwargs):
        """
        Handler for request Product endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request Product endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request Product endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request Product endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)


class PhoneNumberTypeHandler(CRUDHandler):
    """
    Phone Number Type handler
    """
    helper = PhoneNumberType

    def get(self, *args, **kwargs):
        """
        Handler for request Phone Number Type endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request Phone Number Type endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request Phone Number Type endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request Phone Number Type endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)


class ManufacturerHandler(CRUDHandler):
    """
    Manufacturer handler
    """
    helper = Manufacturer

    def get(self, *args, **kwargs):
        """
        Handler for request Manufacturer endpoint with HTTP method GET.

        :param set args: unnamed arguments
        :param dict kwargs: named arguments

        :return: None
        :rtype: None
        """
        self.get_handler(self.helper)

    def post(self):
        """
        Handler for request Manufacturer endpoint with HTTP method POST.

        :return: None
        :rtype: None
        """
        self.post_handler(self.helper)

    def put(self):
        """
        Handler for request Manufacturer endpoint with HTTP method PUT.

        :return: None
        :rtype: None
        """
        self.put_handler(self.helper)

    def delete(self):
        """
        Handler for request Manufacturer endpoint with HTTP method DELETE.

        :return: None
        :rtype: None
        """
        self.delete_handler(self.helper)
