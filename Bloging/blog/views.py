from distutils.log import Log
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post_blog
from django.contrib.auth.models import Group


# Home view

def home(request):
    posts = Post_blog.objects.all()
    return render(request, 'home.html', {'posts':posts})

# Dashboard view

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post_blog.objects.all()
        user = request.user
        fullName = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'dashboard.html', {'posts':posts, 'fullName':fullName, 'groups':gps})
    else:
        return HttpResponseRedirect('/signin/')

# Register view

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Successfully Signed Up !!')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
     form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

# Login view

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'signin.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Logout view

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Add New Blog
def add_new_blog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                created_Date = form.cleaned_data['created_Date']
                owner = form.cleaned_data['owner']
                desc = form.cleaned_data['desc']
                is_Published = form.cleaned_data['is_Published']
                pst = Post_blog(title=title, created_Date=created_Date, owner=owner, desc=desc, is_Published=is_Published)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'add_new_blog.html', {'form':form})
    else:
        return HttpResponseRedirect('/signin/')

# Update Blog
def edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post_blog.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post_blog.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'edit.html', {'form':form})
    else:
        return HttpResponseRedirect('/signin/')

# delete Blog
def delete_blog(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post_blog.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/signin/')