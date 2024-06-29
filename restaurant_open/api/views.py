from django.http import JsonResponse

def restaurant_list(request):
    return JsonResponse({"data": ["McDonalds", "Bubger King"]})