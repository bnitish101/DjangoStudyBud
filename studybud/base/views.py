# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Learn Python'},
#     {'id':2, 'name':'Learn Django'},
#     {'id':3, 'name':'Learn ReactJs'},
#     {'id':4, 'name':'Learn Flask'},
# ]

def home(request):
    # context = {'rooms':rooms}
    rooms = Room.objects.all()
    print('-----------')
    print(rooms)
    print('-----------')
    context = {'rooms':rooms}
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
