from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task
from .forms import TaskForm


@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user)
    context = {'tasks': tasks}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def task(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'task-detail.html', context)


@login_required(login_url='login')
def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'task-form.html', context)


@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'task-form.html', context)


@login_required(login_url='login')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('home')

    context = {'task': task}

    return render(request, 'task-delete.html', context)


########################
## LOGIN AND REGISTER ##
########################

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'User created successfully')
            return redirect('home')
        else:
            messages.error(request, 'An error ocurred during registration')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
