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


