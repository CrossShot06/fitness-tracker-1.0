import json
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta, datetime
from django.core.serializers.json import DjangoJSONEncoder
from .forms import CreateUserForm,UpdateUserForm,TrainerRequestForm,ReviewForm,StepEntryForm,AppointmentForm,WorkoutForm,TargetForm
from .models import Profile,TrainerRequest,Review,StepEntry,Appointments,Workouts,DailyEntry,Target
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
            return redirect('page-redirect')
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
    if request.user.groups.exists():

        group = request.user.groups.all()[0].name

        if group == 'user':

            return redirect('user')
        
        elif group == 'trainer':

            return redirect('trainer')
        
        elif group == 'admin':

            return redirect('/admin/')

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])

def trainer_assign(request):

    trainers = Profile.objects.filter(role = 'trainer')

    context = {
        'trainers':trainers
    }

    return render(request,'accounts/trainer_assign.html',context)

@never_cache
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

@never_cache
@login_required
@allowed_users(allowed_roles=['admin','user'])
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


@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def trainer_reviews_view(request):
    if request.user.profile.role != 'trainer':
        return redirect('home')  
    
    reviews = Review.objects.filter(trainer=request.user).order_by('-created_at')

    return render(request, 'accounts/trainer_reviews.html', {
        'reviews': reviews
    })

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def dashboard(request):
    user = request.user
    today_date = date.today()
    today_name = today_date.strftime("%A")

    DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    selected_day_name = request.POST.get('day') or request.GET.get('day', today_name)

    workouts_for_selected_day = Workouts.objects.filter(trainee=user, day__iexact=selected_day_name)
    workouts_for_today = Workouts.objects.filter(trainee=user, day__iexact=today_name)

    entry, _ = DailyEntry.objects.get_or_create(user=user, date=today_date)

    target, _ = Target.objects.get_or_create(user=user)

    target_form = TargetForm(instance=target)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'daily_entry':

            entry.calories = request.POST.get('calories', entry.calories)
            entry.steps = request.POST.get('steps', entry.steps)
            entry.heartrate = request.POST.get('heartrate', entry.heartrate)
            entry.water = request.POST.get('water', entry.water)
            entry.sleep = request.POST.get('sleep', entry.sleep)

            workout_data = entry.workout_data or {}
            for workout in workouts_for_today:
                sets_value = request.POST.get(f'workout_{workout.id}')
                if sets_value:
                    try:
                        workout_data[str(workout.id)] = int(sets_value)
                    except ValueError:
                        pass
            entry.workout_data = workout_data
            entry.save()

            return redirect(f"{request.path}?day={selected_day_name}")

        elif form_type == 'target_form':
            
            target_form = TargetForm(request.POST, instance=target)
            if target_form.is_valid():
                saved_target = target_form.save(commit=False)
                saved_target.user = request.user
                saved_target.save()
                return redirect(request.path)  

    todays_data = {
        'calories': entry.calories,
        'steps': entry.steps,
        'heartrate': entry.heartrate,
        'workout_data': entry.workout_data,
        'sleep' : entry.sleep,
        'water' : entry.water,
 
    }

    start_date = today_date - timedelta(days=29)
    entries = DailyEntry.objects.filter(
        user=user,
        date__range=(start_date, today_date)
    ).order_by('date')

    date_to_data = {e.date: {"steps": e.steps or 0, "calories": e.calories or 0} for e in entries}
    serialized_chart_data = []

    for i in range(30):
        d = start_date + timedelta(days=i)
        day_data = date_to_data.get(d, {"steps": 0, "calories": 0})
        
        
        workout_entry = next((e for e in entries if e.date == d), None)
        progress = 0.0

        if workout_entry and workout_entry.workout_data:
            workout_data = workout_entry.workout_data
            day_name = d.strftime("%A")
            assigned_workouts = Workouts.objects.filter(trainee=user, day__iexact=day_name)
            total_target_sets = sum(w.sets for w in assigned_workouts)
            total_done_sets = sum(int(workout_data.get(str(w.id), 0)) for w in assigned_workouts)
            if total_target_sets > 0:
                progress = round((total_done_sets / total_target_sets) * 100, 2)

        serialized_chart_data.append({
            'date': d.strftime("%Y-%m-%d"),
            'steps': day_data["steps"],
            'calories': day_data["calories"],
            'workout_progress': progress
        })

    if not serialized_chart_data:
        serialized_chart_data = []

    confirmed_appointments = Appointments.objects.filter(
        trainee=user,
        status="CONFIRMED"
    )
    events = [
        {
            "title": f"{a.description} with {a.trainer.username}",
            "start": a.start_datetime.isoformat(),
            "end": a.end_datetime.isoformat()
        }
        for a in confirmed_appointments
    ]

    if not events:
        events = []




    context = {

        'chart_data_json': serialized_chart_data,
        'events_json': events,
        'workouts': workouts_for_selected_day,
        'today_workouts': workouts_for_today,
        'selected_day': selected_day_name,
        'days': DAYS_OF_WEEK,
        'today_name': today_name,
        'todays_data': todays_data,
        'is_today': (selected_day_name == today_name),
        'form': target_form,
        'target':target

    }

    return render(request, 'accounts/dashboard.html', context)

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
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

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
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

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
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

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def view_users(request):

    users = Profile.objects.filter(role='user')
    return render(request, 'accounts/view_user.html', {'users': users})

@never_cache
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def trainer_view_user_dashboard(request, username):

    target_user = get_object_or_404(User, username=username)
    today_date = date.today()
    today_name = today_date.strftime("%A")
    DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    selected_day_name = request.GET.get('day', today_name)

    workouts_for_selected_day = Workouts.objects.filter(trainee=target_user, day__iexact=selected_day_name)
    workouts_for_today = Workouts.objects.filter(trainee=target_user, day__iexact=today_name)

    entry, _ = DailyEntry.objects.get_or_create(user=target_user, date=today_date)
    target, _ = Target.objects.get_or_create(user=target_user)
    target_form = TargetForm(instance=target)

    todays_data = {
        'calories': entry.calories,
        'steps': entry.steps,
        'heartrate': entry.heartrate,
        'workout_data': entry.workout_data,
        'sleep': entry.sleep,
        'water': entry.water,
    }

    start_date = today_date - timedelta(days=29)
    entries = DailyEntry.objects.filter(user=target_user, date__range=(start_date, today_date)).order_by('date')

    date_to_data = {e.date: {"steps": e.steps or 0, "calories": e.calories or 0} for e in entries}
    serialized_chart_data = []

    for i in range(30):
        d = start_date + timedelta(days=i)
        day_data = date_to_data.get(d, {"steps": 0, "calories": 0})
        progress = 0.0

        workout_entry = next((e for e in entries if e.date == d), None)
        if workout_entry and workout_entry.workout_data:
            workout_data = workout_entry.workout_data
            day_name = d.strftime("%A")
            assigned_workouts = Workouts.objects.filter(trainee=target_user, day__iexact=day_name)
            total_target_sets = sum(w.sets for w in assigned_workouts)
            total_done_sets = sum(int(workout_data.get(str(w.id), 0)) for w in assigned_workouts)
            if total_target_sets > 0:
                progress = round((total_done_sets / total_target_sets) * 100, 2)

        serialized_chart_data.append({
            'date': d.strftime("%Y-%m-%d"),
            'steps': day_data["steps"],
            'calories': day_data["calories"],
            'workout_progress': progress
        })

    confirmed_appointments = Appointments.objects.filter(
        trainee=target_user,
        status="CONFIRMED"
    )
    events = [
        {
            "title": f"{a.description} with {a.trainer.username}",
            "start": a.start_datetime.isoformat(),
            "end": a.end_datetime.isoformat()
        }
        for a in confirmed_appointments
    ]

    context = {
        'chart_data_json': serialized_chart_data,
        'events_json': events,
        'workouts': workouts_for_selected_day,
        'today_workouts': workouts_for_today,
        'selected_day': selected_day_name,
        'days': DAYS_OF_WEEK,
        'today_name': today_name,
        'todays_data': todays_data,
        'is_today': (selected_day_name == today_name),
        'form': target_form,
        'target': target,
        'readonly': True,  
        'target_user': target_user,
    }

    return render(request, 'accounts/trainer_dashboard.html', context)

