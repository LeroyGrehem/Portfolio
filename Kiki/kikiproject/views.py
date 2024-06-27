from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, ProjectForm, Profile, UpdateForm
from .models import UserProfile, Project
from django.shortcuts import get_object_or_404
# # Create your views here.


def home(request):
    # Check to see if logging in
    projects = Project.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    #     Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("You Have Been Logged In!")
            return redirect('home')
        else:
            print("There Was An Error Loggin In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'projects': projects})


def users_profile(request, pk):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=pk)
        projects = Project.objects.filter(user_id=pk).order_by('-created_at')
        return render(request, 'users_profile.html', {'profile': profile, 'projects': projects})

    else:
        print("You must be logged in...")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = UserProfile.objects.get(user=current_user)

        # Instantiate forms with request data and model instances
        user_form = UpdateForm(request.POST or None, instance=current_user, required=False)
        profile_form = Profile(request.POST or None, request.FILES or None, instance=profile_user, required=False)

        if request.method == 'POST':
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                # Re-login the user to update session data
                login(request, current_user)
                print("Your info has been updated")
                return redirect('home')
            else:
                print("There is a problem...")
                print(user_form.errors)
                print(profile_form.errors)

        return render(request, "update_profile.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        print("You must be logged in")
        return redirect('home')



def logout_user(request):
    logout(request)
    print("You have been logged out")
    return redirect('home')


# def project_page(request):
    # return render(request, 'project_page.html')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
        #     Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            print("You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def new_project(request):
    if request.user.is_authenticated:
        form = ProjectForm(request.POST, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user
                project.save()
                print("Project Add Successfully...")
                return redirect('home')
            else:
                print("Form is not valid")
        return render(request, 'new_project.html', {'form': form})
    else:
        print("You Must Be Logged In...")
        return redirect('home')


def view_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    if project:
        return render(request, 'project.html', {'project': project})
    else:
        print("That project does not exist...")
        return redirect('home')
