from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddExerciseForm, AddPlanForm
from .models import Exercise, Plan
from django.utils import timezone


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        plans = Plan.objects.filter(created_by=request.user)
        exercises = Exercise.objects.filter(created_by=request.user)
    else:
        plans = []
        exercises = []

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
        return render(request, 'home.html', {'exercises': exercises, 'plans': plans})


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


def plan_record(request, pk):
    if request.user.is_authenticated:
        plan = Plan.objects.get(id=pk)
        return render(request, 'plan.html', {'plan': plan})
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


def delete_plan(request, pk):
    if request.user.is_authenticated:
        delete_it = Plan.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Plan has been deleted.')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')


def add_exercise(request):
    form = AddExerciseForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                exercise = form.save(commit=False)
                exercise.created_by = request.user
                exercise.save()
                messages.success(request, 'Exercise has been added.')
                return redirect('home')
        return render(request, 'add_exercise.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')


def add_plan(request):
    form = AddPlanForm(request.POST or None, user=request.user)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                plan = form.save(commit=False)
                plan.created_by = request.user
                plan.save()
                form.save_m2m()
                return redirect("home")
        return render(request, 'add_plan.html', {'form': form})
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


def update_plan(request, pk):
    if request.user.is_authenticated:
        current_plan = Plan.objects.get(id=pk)
        form = AddPlanForm(request.POST or None, instance=current_plan, user=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            form.save_m2m()
            messages.success(request, 'Plan has been updated.')
            return redirect('home')
        return render(request, 'update_plan.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')


def execute_plan(request, pk):
    if request.user.is_authenticated:
        plan = Plan.objects.get(id=pk, created_by=request.user)
        plan.last_executed = timezone.now()
        plan.save()
        messages.success(request, 'Plan has been executed.')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to do that action.')
        return redirect('home')