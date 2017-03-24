import hashlib, uuid

from google.appengine.ext import db

from model import PersonModel


class Person(object):
    def save_person(self, firstname, lastname, username, email, password, id):
        person = PersonModel()
        person.firstname = firstname
        person.lastname = lastname
        person.username = username
        person.email = email
        person.password = self.encrypt_password(password)
        person.put()

    def delete_person(self, person_ids):
        if len(person_ids) > 0:
            for person_id in person_ids:
                person_k = db.Key.from_path('PersonModel', long(person_id))
                person = db.get(person_k)
                db.delete(person_k)

    def auth_list_person(self):
        result = []
        person = PersonModel.all()
        for i in person:
            result.append(
                {
                    'username': i.username,
                    'password': i.password,
                }
            )
        return result

    def list_person(self):
        result = []
        person = PersonModel.all()
        for i in person:
            result.append(
                {
                    'firstname': i.firstname,
                    'lastname': i.lastname,
                    'username': i.username,
                    'email': i.email,
                }
            )
        return result

    def encrypt_password(self, password):
        return hashlib.sha512(password).hexdigest()
