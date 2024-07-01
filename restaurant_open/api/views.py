from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import RestaurantHours
from . import util


ROLLOVER_TIME = 4

def restaurant_list(request):
    try:
        datetime_obj = datetime.strptime(request.GET.get("datetime"), "%b %d %Y %I:%M%p")
    except ValueError:
        try:
            datetime_obj = datetime.strptime(request.GET.get("datetime"), "%b %d %Y %I%p")
        except ValueError:
            return JsonResponse({"error":"Invalid date format. Please format date as such: Jan 1 2024 11:30pm"}, status=400)


    all_restaurants = RestaurantHours.objects.all()
    open_restaurants = []

    for rest in all_restaurants:

        prev_hours = None
        hours = util.fetch_hours(datetime_obj.weekday(), rest)

        # The "ROLLOVER_TIME" is a bit arbitrary, but essentially, if I am checking for
        # restaurants at "Monday 2am", I actually need to check Sunday's hours
        if datetime_obj.hour <= ROLLOVER_TIME:
            prev_hours = util.fetch_hours(util.decrement_weekday(datetime_obj.weekday()), rest)

            if prev_hours == "closed":
                continue
            
            # Need to convert "hours" to workable datetime objects
            start_time = prev_hours.split('-')[0].strip()
            end_time = prev_hours.split('-')[1].strip()
        else:
            if hours == "closed":
                continue
            start_time = hours.split('-')[0].strip()
            end_time = hours.split('-')[1].strip()



        try:
            start_time = datetime.strptime(start_time, "%I:%M %p")
        except ValueError:
            try:
                start_time = datetime.strptime(start_time, "%I %p")
            except ValueError:
                raise Exception("Invalid time format")
            
        try:
            end_time = datetime.strptime(end_time, "%I:%M %p")
        except ValueError:
            try:
                end_time = datetime.strptime(end_time, "%I %p")
            except ValueError:
                raise Exception("Invalid time format")
            
        start_time = datetime_obj.replace(hour=start_time.hour, minute=start_time.minute)
        end_time = datetime_obj.replace(hour=end_time.hour, minute=end_time.minute)

        # Bump back start time to previous day if necessary
        if datetime_obj.hour <= ROLLOVER_TIME:
            start_time = start_time - timedelta(days=1)
            end_time = end_time - timedelta(days=1)
        # If the "Closing time" is actually the next day, that needs to be reflected
        # before comparison occurs    
        if end_time.hour <= ROLLOVER_TIME:
            end_time = end_time + timedelta(days=1)

        if hours != "closed" and start_time <= datetime_obj and end_time >= datetime_obj:
            open_restaurants.append(rest.name)

    return JsonResponse({"data": open_restaurants})