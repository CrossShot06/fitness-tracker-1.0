from django.shortcuts import render


def home(request):
    return render(request,"accounts/home.html")


def user(request):
    return render(request,"accounts/user.html")

def trainer(request):
    return render(request,"accounts/user.html")


