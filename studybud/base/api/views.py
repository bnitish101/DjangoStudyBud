# from django.http import JsonResponse

# def getRoutes(request):
#     routes = [
#         'GET /api',
#         'GET /api/room',
#         'GET /api/room/:id',
#     ]

#     return JsonResponse(routes, safe=False)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from base.api.serializer import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    print('----------------serializer----------------')
    print(serializer.data)
    print('----------------serializer----------------')
    return Response(serializer.data)

@api_view(['get'])
def getRoom(request, pk):
    room = Room.objects.get(pk=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)