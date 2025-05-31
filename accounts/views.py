from django.shortcuts import render, redirect
from .forms import CreateUserForm,UpdateUserForm,TrainerRequestForm
from .models import Profile,TrainerRequest
from .decorators import unautheticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import HttpResponse


@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, "accounts/home.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def user(request):
    form=UpdateUserForm(instance=request.user.profile)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES , instance=request.user.profile)
        if form.is_valid():
            form.save()

    context = {'form' : form}
    return render(request, "accounts/user.html" , context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def trainer(request):
    return render(request, "accounts/trainer.html")

@never_cache
@unautheticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')


            Profile.objects.create(user=user, role=role, username=username, email=email)

            group = Group.objects.get(name=role)
            user.groups.add(group)

            return redirect('login')

    context = {'form': form}
    return render(request, "accounts/register.html", context)

@never_cache
@unautheticated_user
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username Or Password is Incorrect')
    context={}
    return render(request,'accounts/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def trainer_request(request):

    success = False

    form = TrainerRequestForm()
    
    if request.method == 'POST':
        form = TrainerRequestForm(request.POST)
        if form.is_valid():

            trainer_request = form.save(commit=False)
            trainer_request.user = request.user
            trainer_request.save()

            success = True
        

    context={'form':form,'success':success}

    return render(request,'accounts/trainer_request.html',context)



