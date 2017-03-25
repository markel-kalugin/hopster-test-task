import logging
import webapp2
from webapp2_extras import sessions
from helpers import Person
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
                error_message='Person does not exists'
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
            input_firstname = params['firstname']
            input_lastname = params['lastname']
            input_username = params['username']
            input_email = params['email']
            input_password = params['password']
            person = Person()
            person.save_person(
                input_firstname,
                input_lastname,
                input_username,
                input_email,
                input_password
            )
            logging.info('User with username {} was created.'.format(input_username))
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
            input_id = params['id']
            input_firstname = params['firstname']
            input_lastname = params['lastname']
            input_username = params['username']
            input_email = params['email']
            input_password = params['password']
            person = Person()
            person.update_person(
                input_firstname,
                input_lastname,
                input_username,
                input_email,
                input_password,
                input_id
            )
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

