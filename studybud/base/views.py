from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Learn Python'},
#     {'id':2, 'name':'Learn Django'},
#     {'id':3, 'name':'Learn ReactJs'},
#     {'id':4, 'name':'Learn Flask'},
# ]

def loginPage(request): # do not make login() method because already created one by django admin
    page = 'login'
    # ----------- cb+ s (check is user already logged in) ----------- #
    if request.user.is_authenticated:
        return redirect('home')
    # ----------- cb+ e (check is user already logged in) ----------- #

    if request.method == 'POST':
        print(request.POST)
        # username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            # user = User.objects.get(username=username)
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')

        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user) # this will set the session id data
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # page = 'register'
    # form = UserCreationForm()
    form = MyUserCreationForm()

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = MyUserCreationForm(request.POST)
        print('------------')
        print(form.is_valid)
        print('------------')
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error encounterd during the registration!')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def profilePage(request, pk):
    users = User.objects.get(id=pk)
    rooms  = users.room_set.all()
    room_messages = users.message_set.all()
    all_topics_count = Topic.objects.all().count()
    topics = Topic.objects.all()[0:5]
    print('---------------------')
    print(room_messages.query)
    print('---------------------')
    context = {'users':users, 'rooms': rooms, 'room_messages':room_messages, 'topics':topics, 'all_topics_count':all_topics_count}
    return render(request, 'base/profile.html', context)

def home(request):
    print('------------- cb+ s (print user data) -------------')
    print(request.user)
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    print('------------- cb+ e (print user data) ------------- ')
    # context = {'rooms':rooms}
    all_topics_count = Topic.objects.all().count()
    
    print('---------------------- all_topics_count----------------------')
    print(all_topics_count)
    print('---------------------- all_topics_count----------------------')
    
    topics = Topic.objects.all()[0:5]
    
    # rooms = Room.objects.all()

    # it will check if q is not None then don't set get parameter eg. isset get parameter
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # ----------- cb+ s (search query with single field) ----------- #
    # icontains will check at least match with q values with case insenstive, contains will check with case sentive
    # double underscore becase need to match data from <Topic> parent table of <Room> table
    # rooms = Room.objects.filter(topic__name__icontains=q)
    # ----------- cb+ e (search query with single field) ----------- #
    
    # ----------- cb+ s (search query with multiple fields) ----------- #
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    # ----------- cb+ e (search query with multiple fields) ----------- #
    
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q)) # parent of parent data fetch [Message table >> Room table >> Topic table]

    print('-----------')
    print(rooms)
    print('-----------')
    context = {'rooms':rooms, 'topics':topics, "all_topics_count":all_topics_count, 'room_count': room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # room = None
    # for i in rooms:
        # print('-----------')
        # print(rooms)
        # print('-----------')
        # print(i)
        # print('-----------')
        # print(type(i))
        # print('-----------')
        # if i['id'] == int(pk):
            # room = i['name']

    # context = {'room': room}
    room = Room.objects.get(id=pk)
    print('-----------')
    print(room)
    print(room.name)
    print(room.description)
    print('-----------')
    room_message = room.message_set.all().order_by('-created') # fetch the all data from child table by parent's table id 
    participants = room.participants.all() # data fetch from many to mayn relationship
    print('-----------')
    print(participants)
    print('-----------')
    # ----------- cb+ s (add comments) ----------- #
    if request.method == 'POST':
        # insert data into <Message> table fields 
        message = Message.objects.create( 
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id) # this will reload the page
    # ----------- cb+ e (add comments) ----------- #

    context = {'room': room, 'room_message': room_message, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login') # Before createRoom(request), user login check if not login redirect to the login page
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')  
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        
        # print(request.POST)
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False);
        #     room.host = request.user
        #     room.save()
            
            # return redirect('home')

    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):

    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # -------------- cb+ s (check the user id is match with user's id in the room to be updated) -------------- #
    if request.user != room.host:
        return HttpResponse('You are not allowed to here!!!!!')
    # -------------- cb+ e (check the user id is match with user's id in the room to be updated) -------------- #

    print('------ cb+ 1 ------')
    if request.method == 'POST':
        print('------ cb+ 2 ------')
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # room.host = request.user
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room)

        # if form.is_valid():
        #     print('------ cb+ 3 ------')
        #     form.save()
        #     return redirect('home')
    
    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # -------------- cb+ s -------------- #
    if request.user != room.host:
        return HttpResponse('You are not allowed to here!!!!!')
    # -------------- cb+ e -------------- #

    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    # -------------- cb+ s -------------- #
    if request.user != message.user:
        return HttpResponse('You are not allowed to here!!!!!')
    # -------------- cb+ e -------------- #

    if request.method == 'POST':
        message.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()

            return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/update_user.html', context)

def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)