import json
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta, datetime
from django.core.serializers.json import DjangoJSONEncoder
from .forms import CreateUserForm,UpdateUserForm,TrainerRequestForm,ReviewForm,StepEntryForm,AppointmentForm,WorkoutForm
from .models import Profile,TrainerRequest,Review,StepEntry,Appointments,Workouts
from django.contrib.auth.models import User
from .decorators import unautheticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from chat_rt.models import ChatGroup

@never_cache
@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, "accounts/home.html")

@never_cache
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


@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def trainer(request):
    
    form=UpdateUserForm(instance=request.user.profile)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES , instance=request.user.profile)
        if form.is_valid():
            form.save()

    context = {'form' : form}
    return render(request, "accounts/trainer.html", context)

@never_cache
@unautheticated_user
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = Group.objects.get(name = 'user')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')


            Profile.objects.create(user=user, role=role, username=username, email=email)

            user.groups.add(role)

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

@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')

@never_cache
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

@login_required(login_url='login')
def page_redirect(request):
    
    group = None

    if request.user.groups.exist():

        group = request.user.groups.all()[0].name

        if group == 'user':

            return redirect('user')
        
        elif group == 'trainer':

            return redirect('trainer')
        
        else:

            return redirect('home')


@login_required(login_url='login')
def trainer_assign(request):

    trainers = Profile.objects.filter(role = 'trainer')

    context = {
        'trainers':trainers
    }

    return render(request,'accounts/trainer_assign.html',context)

@login_required(login_url='login')
def inbox(request):
    my_profile = request.user.profile
    chatrooms = my_profile.chat_group.all()

    chat_summaries=[]

    if chatrooms.exists():
        for chat in chatrooms:
            for member in chat.members.all():
                if member !=my_profile:
                    other_user = member
                    break
            last_message = chat.chat_messages.last()
            chat_summaries.append({
                'chat':chat,
                'other_user':other_user,
                'last_message':last_message,
            })
    context = {
        'chat_summaries':chat_summaries
    }

    return render(request,'accounts/inbox.html',context)

@login_required
def reviews_page(request,username):
    trainer = get_object_or_404(User,username=username)
    reviews = Review.objects.filter(trainer=trainer).order_by('-created_at')

    if trainer.profile.role != 'trainer':
        return redirect('home')  
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.trainer = trainer
            review.save()
            return redirect('reviews_page', username=trainer.username)

    else:
        form = ReviewForm()

    return render(request, 'accounts/reviews_page.html', {
        'form': form,
        'reviews': reviews
    })


@login_required
def trainer_reviews_view(request):
    if request.user.profile.role != 'trainer':
        return redirect('home')  
    
    reviews = Review.objects.filter(trainer=request.user).order_by('-created_at')

    return render(request, 'accounts/trainer_reviews.html', {
        'reviews': reviews
    })

@login_required
def dashboard(request):

    today = date.today()
    start_date = today - timedelta(days=29)  


    entries = StepEntry.objects.filter(
        user=request.user,
        date__range=(start_date, today)
    ).order_by('date')

    date_to_steps = {e.date: e.steps for e in entries}


    serialized_entries = []
    for i in range(30):
        d = start_date + timedelta(days=i)
        steps = date_to_steps.get(d, 0)
        serialized_entries.append({
            'date': d.strftime("%Y-%m-%d"), 
            'steps': steps
        })

    step_data_json = json.dumps(serialized_entries, cls=DjangoJSONEncoder)

    confirmed_appointments = Appointments.objects.filter(
        trainee = request.user,
        status = "CONFIRMED"
    )

    events = [
        {
            "title": f"{a.description} with {a.trainer.username}",
            "start": a.start_datetime.isoformat(),
            "end": a.end_datetime.isoformat()
        }
        for a in confirmed_appointments
    ]

    events_json = json.dumps(events,cls=DjangoJSONEncoder)

    user = request.user
    today = datetime.today().strftime('%A') 

    workouts = Workouts.objects.filter(trainee=user, day__iexact=today)

    print(workouts)

    context = {
        'step_data_json': step_data_json,
        'events_json': events_json,
        'workouts':workouts
    }

    return render(request, 'accounts/dashboard.html', context)


def set_goals(request):

    form = StepEntryForm()
    
    if request.method == 'POST':
        form = StepEntryForm(request.POST)
        if form.is_valid():

            steps = form.save(commit=False)
            steps.user = request.user
            
            steps.save()
    
    context = {
        'form':form
    }

    return render(request,'accounts/set_goals.html',context)

def request_appointment(request,username):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.trainer = get_object_or_404(User,username=username)
            appointment.trainee = request.user
            appointment.status = 'PENDING'
            appointment.save()
    else:
        form = AppointmentForm()
    return render(request, 'accounts/appointments_request.html', {'form': form})

def trainer_appointments(request):
    trainer = request.user
    pending_appointments = Appointments.objects.filter(trainer=trainer, status='PENDING')

    confirmed_appointments = Appointments.objects.filter(
        trainer = request.user,
        status = "CONFIRMED"
    )

    events = [
        {
            "title": f"{a.description} with {a.trainee.username}",
            "start": a.start_datetime.isoformat(),
            "end": a.end_datetime.isoformat()
        }
        for a in confirmed_appointments
    ]

    events_json = json.dumps(events,cls=DjangoJSONEncoder)

    context={
        'pending_appointments':pending_appointments,
        'events_json':events_json
    }

    return render(request,'accounts/trainer_appointment.html',context)

def approve_appointment(request,appointment_id):
    appointment = get_object_or_404(Appointments,pk=appointment_id,trainer=request.user)
    appointment.status = 'CONFIRMED' 
    appointment.save()
    return redirect('trainer_appointments')

def reject_appointment(request,appointment_id):
    appointment = get_object_or_404(Appointments,pk=appointment_id,trainer=request.user)
    appointment.status = 'REJECTED' 
    appointment.save()
    return redirect('trainer_appointments')

def assign_workout(request):

    if request.method == 'POST':
        form = WorkoutForm(request.POST,request.FILES)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.trainer = request.user
            workout.save()
            return redirect('assign_workout')
    else:
        form = WorkoutForm()
    
    context = {
        'form':form
    }

    return render(request,'accounts/assign_workout.html',context)