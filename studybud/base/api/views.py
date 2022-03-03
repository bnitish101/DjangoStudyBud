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

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/room',
        'GET /api/room/:id'
    ]
    return Response(routes)