# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Learn Python'},
#     {'id':2, 'name':'Learn Django'},
#     {'id':3, 'name':'Learn ReactJs'},
#     {'id':4, 'name':'Learn Flask'},
# ]

def loginPage(request): # do not make login() method because already created one by django admin
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # this will set the session id data
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {}
    return render(request, 'base/login_register.html', context)

def home(request):
    # context = {'rooms':rooms}
    topics = Topic.objects.all()
    
    # rooms = Room.objects.all()

    # it will check if q is not None the don't set get parameter eg. isset get parameter
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

    print('-----------')
    print(rooms)
    print('-----------')
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count}
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
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm();
    if request.method == 'POST':
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save();
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    print('------ cb+ 1 ------')
    if request.method == 'POST':
        print('------ cb+ 2 ------')
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            print('------ cb+ 3 ------')
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html', {'obj': room})