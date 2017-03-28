import webapp2
import logging
import json

from scripts.handlers import (
    AuthenticationHandler, UserManagementHandler, CompanyHandler, CompanyBrandHandler,
    ProductCategoryHandler, ProductHandler, PhoneNumberTypeHandler, ManufacturerHandler
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
    ('/api/v1/users', UserManagementHandler),
    ('/api/v1/company', CompanyHandler),
    ('/api/v1/company_brand', CompanyBrandHandler),
    ('/api/v1/product_category', ProductCategoryHandler),
    ('/api/v1/product', ProductHandler),
    ('/api/v1/phone_number_type', PhoneNumberTypeHandler),
    ('/api/v1/manufacturer', ManufacturerHandler),
], debug=True, config=config)
# application.error_handlers[404] = handle_error
# application.error_handlers[500] = handle_error
