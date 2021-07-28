from django.db import models
import re
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey
import bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name needs to be at least 2 characters."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name needs to be at least 2 character."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ('Invalid email address!')
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = 'Passwords do not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def register(postData):
        password = postData['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=pw_hash)


class WishManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['wish_name']) < 5:
            errors['wish_name'] = 'Your wish needs at least 5 characters.'
        if len(postData['description']) < 5:
            errors['description'] = 'Your description of your wish has to be at least 5 characters.'
        return errors
        
class Wish(models.Model):
    wish_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    granted = BooleanField(False)
    # make a fnc to add granted_date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
    wish_user = ForeignKey(User, related_name='user', on_delete=CASCADE)
    # in order to dot notate it in template put the user in a context to your template then iterate through all the wishes and check if the wish_user == user.id