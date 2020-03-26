from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def reg(request):
    errors = User.objects.validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    is_user_in_db = User.objects.filter(email = request.POST['email']).first() # if already existing will return an objects of a user

    if is_user_in_db:
        print("user is already exsiting")
        return redirect("/")
    
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user_created = User.objects.create(
        first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        email = request.POST['email'],
        password = hashed_pw
    )

    request.session['user_id'] = user_created.id

    return redirect('/success')

def success(request):
    user_id_is_session = request.session.get('user_id')

    if user_id_is_session:
        user_from_db = User.objects.get(id = user_id_is_session)
        context = {
            "user": user_from_db,
            "all_messages" : Message.objects.all().order_by("-created_at") # Gets all the messages from the database
        }
        return render(request, "success.html", context)
    return redirect("/")

def log(request):
    errors = User.objects.logginValidator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    found_user = User.objects.filter(email = request.POST['email']).first()

    if found_user: # if email is found in db
        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(),
            found_user.password.encode()
        )

        if is_pw_correct: # if password is correct
            request.session['user_id'] = found_user.id
            return redirect('/success')
        else: #if pw is incorrect
            print("something is not working")
            return redirect("/")
    else: # if email is not found
        print("something is not working")
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def message(request): #POST
    errors = Message.objects.MessageValidator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/success") # this is where the form that caused the error is in

    user_id_in_session = request.session.get('user_id')

    if user_id_in_session:
        user_from_db = User.objects.get(id = user_id_in_session)

        Message.objects.create(
            message = request.POST['message'],
            user_posted = user_from_db
        )

        return redirect("/success")

    return redirect("/")

def comment(request, id):
    errors = Comment.objects.ComementValidator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/success")

    user_id_in_session = request.session.get('user_id')

    if user_id_in_session:
        user_from_db = User.objects.get(id = user_id_in_session)

        message_commented = Message.objects.get(id = id)

        Comment.objects.create(
            comment = request.POST['comment'],
            user_posted = user_from_db,
            message_posted_on = message_commented
        )

        return redirect("/success")

    return redirect("/")

def like(request, id):
    user_id_in_session = request.session.get('user_id')

    if user_id_in_session:
        user_from_db = User.objects.get(id = user_id_in_session)
        message_likes = Message.objects.get(id = id)
        message_likes.likes.add(user_from_db)
        return redirect("/success")

    return redirect("/")


