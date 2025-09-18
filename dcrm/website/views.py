from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddExerciseForm
from .models import Exercise


# Create your views here.
def home(request):
    exercises = Exercise.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    else:
        return render(request, 'home.html', {'exercises': exercises})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You are now registered.')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def exercise_record(request, pk):
    if request.user.is_authenticated:
        exercise = Exercise.objects.get(id=pk)
        return render(request, 'exercise.html', {'exercise': exercise})
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('home')

def delete_exercise(request, pk):
    if request.user.is_authenticated:
        delete_it = Exercise.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Exercise has been deleted.')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')

def add_exercise(request):
    form = AddExerciseForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_exercise = form.save()
                messages.success(request, 'Exercise has been added.')
                return redirect('home')
        return render(request, 'add_exercise.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')

def update_exercise(request, pk):
    if request.user.is_authenticated:
        current_exercise = Exercise.objects.get(id=pk)
        form = AddExerciseForm(request.POST or None, instance=current_exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exercise has been updated.')
            return redirect('home')
        return render(request, 'update_exercise.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')