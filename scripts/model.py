from google.appengine.ext import db


class PersonModel(db.Model):
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    username = db.StringProperty()
    email = db.StringProperty()
    password = db.StringProperty()
