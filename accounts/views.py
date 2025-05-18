from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
def home(request):
    return render(request, "accounts/home.html")

def user(request):
    return render(request, "accounts/user.html")

def trainer(request):
    return render(request, "accounts/trainer.html")

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            # Create profile with selected role
            Profile.objects.create(user=user, role=role)

            return redirect('login')

    context = {'form': form}
    return render(request, "accounts/register.html", context)

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')

    context={}
    return render(request,'accounts/login.html',context)