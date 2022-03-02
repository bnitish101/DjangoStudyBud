from django.http import JsonResponse

def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/room',
        'GET /api/room/:id',
    ]

    return JsonResponse(routes, safe=False)