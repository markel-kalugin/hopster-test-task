import webapp2
import logging
import json

from scripts.handlers import (
    AuthenticationHandler, UserManagementHandler
)


def handle_error(request, response, exception):
    response.headers.add_header('Content-Type', 'application/json')
    result = {
        'status': 'error'
    }
    response.write(json.dumps(result))

config = {
    'webapp2_extras.sessions': {'secret_key': 'my_secret'}
}

application = webapp2.WSGIApplication([
    ('/api/v1/authenticate', AuthenticationHandler),
    ('/api/v1/users', UserManagementHandler)
], debug=True, config=config)
application.error_handlers[404] = handle_error
application.error_handlers[500] = handle_error
