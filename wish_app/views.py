from django.shortcuts import render, HttpResponse, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = User.register(request.POST)
        messages.success(request, "Account successfully created!")
        request.session['user_id'] = logged_user.id
        return redirect('/wishes')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/wishes')
    return redirect('/')

def dashboard(request):
    logged_user = User.objects.get(id=request.session['user_id'])
    wish_user = Wish.objects.wish_user.get(id=request.session['user_id'])
    context = {
        'dashboard_user' : logged_user,
        'all_wishes' : Wish.objects.all()

    }
    return render(request, 'dashboard.html', context)

def wishes_new(request):
    context = {
        'wish_user' : logged_user
    }
    return render(request, 'make_a_wish.html', context)

def process_wish(request):
    pass
    # This is where we left off