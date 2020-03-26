from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data): # just for registrations
        errors = {}
        if len(data['fname'])<2:
            errors['fname'] = "First name has to be 2 chars"
        if len(data['lname'])<2:
            errors['lname'] = "Last name has to be 2 chars"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        if data['password']!=data['cpassword']:
            errors['password'] = "Passwords do not match"
        if len(data['password'])<8:
            errors['password'] = "Password is too short"
        return errors

    def logginValidator(self, data):
        errors = {}
        if data['email']=="":
            errors["email"] = "Please enter an email address to log in"
        if data['password']=="":
            errors["password"] = "Please enter an password address to log in"
        return errors

class MessageCommentManager(models.Manager):
    def MessageValidator(self, data):
        errors = {}
        if data['message']=="":
            errors["message"] = "Please enter a value in the message"
        return errors


    def ComementValidator(self, data):
        errors = {}
        if data['comment']=="":
            errors["comment"] = "Please enter a value in the comment"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # an instance of our manager so we can access the validations function

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_posted = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE) # 1:m with user
    likes = models.ManyToManyField(User, related_name="likes") # m:m with message and user
    objects = MessageCommentManager()

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_posted = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE) # 1:m with user
    message_posted_on = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE) # 1:m with message
    objects = MessageCommentManager()