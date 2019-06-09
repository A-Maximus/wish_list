from django.db import models
from datetime import datetime
from time import strptime, localtime
import bcrypt

# Create your models here.


class UserManager(models.Manager):
    def Reg_validator(self, post):
        print(post)
        errors = {}
        if len(post['name']) == 0:
            errors['name'] = "Name cannot be blank!"
        elif len(post["name"]) < 3:
            errors["name"] = "Name must be at least 3 characters"

        if len(post['username']) == 0:
            errors['username'] = "Username cannot be blank!"
        elif len(post['username']) < 3:
            errors['username'] = "Username should be at least 3 characters!"
        else:
            users = User.objects.filter(username=post["username"])
            if users:
                errors["username"] = "Username already exists"
        if len(post["password"]) == 0:
            errors["password"] = "Password cannot be blank!"
        elif len(post["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if len(post["confirm_password"]) == 0:
            errors["confirm_password"] = "Password cannot be blank!"
        elif post["confirm_password"] != post["password"]:
            errors["confirm_password"] = "Passwords must match"

        return errors


    def Login_validator(self, post):
        errors = {}
        print(post)

        if len(post["password"]) == 0:
            errors["password"] = "Password cannot be blank"
        elif post["password"] != post["password"]:
            errors["password"] = "Password is incorrect"

        if len(post["username"]) == 0:
            errors["username"] = "Username cannot be blank"

        else:
            users = User.objects.filter(username=post["username"])
            if not users:
                    errors["username"] = "This username does not exist. Please register!"
            elif not bcrypt.checkpw(post["password"].encode(), users[0].password.encode()):
                    errors["password"] = "Wrong password"

        return errors


class ItemManager(models.Manager):
    def Item_validator(self, post):
        print(post)
        errors = {}
        if len(post['item']) == 0:
            errors['item'] = 'Item field cannot be blank!'
        
        elif len(post['item']) < 4:
            errors['item'] = 'You can wish better than that!!'
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Item(models.Model):
    item = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # description = models.TextField()
    # travel_date_from = models.DateTimeField()
    # travel_date_to = models.DateTimeField()
    objects = ItemManager()


class Join(models.Model):
    user = models.ForeignKey(User, related_name='wish_list',on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='wish_list', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # trip = models.ForeignKey(Trip, related_name='users',on_delete=models.CASCADE)
