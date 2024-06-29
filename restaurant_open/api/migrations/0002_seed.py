from django.db import migrations
import csv
import re

def clear_data(apps, schema_editor):
    # Just clear out any lingering data so it can be reloaded from the CSV
    RestaurantHours = apps.get_model("api", "RestaurantHours")
    RestaurantHours.objects.all().delete()

def seed_data(apps, schema_editor):
    RestaurantHours = apps.get_model("api", "RestaurantHours")
    with open('restaurants.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            rh = RestaurantHours(name=row['Restaurant Name'])
            parse_hours_string(row['Hours'], rh)
            rh.save()


def parse_hours_string(hours, rh):
    # Split if there are multiple times
    hours_split = hours.split('/')

    # Establish list of days for iteration
    weekdays = "Mon Tues Wed Thu Fri Sat Sun".split()
    open_days_list = []


    for hours in hours_split:
        open_days_list.clear()

        # Grab just the days
        days_re = re.search("^(.*?)[0-9]", hours)
        days = days_re[1].strip()

        # Grab just the times
        time_re = re.search("[0-9](.*)", hours)
        time = time_re[0].strip()

        # If the days are split by the comma, split it even further
        days_split = days.split(',')
        for day in days_split:
            if '-' in day:
                day_range = day.split('-')
                open_days_list.append(day_range[0])
                open_days_list.append(day_range[1])

                # Iterate through the days of the week to individually add them all
                for i in range ((weekdays.index(day_range[0].strip())+1), weekdays.index(day_range[1].strip())):
                   open_days_list.append(weekdays[i]) 
            else:
                # If its just a singular day, just add it to the list
                open_days_list.append(day.strip())

        # Go through the list of days and set the time for all of them.
        # Any day not set will default to closed in the DB
        for day in open_days_list:
            match day:
                case "Mon":
                    rh.monday = time
                case "Tues":
                    rh.tuesday = time
                case "Wed":
                    rh.wednesday = time
                case "Thu":
                    rh.thursday = time
                case "Fri":
                    rh.friday = time
                case "Sat":
                    rh.saturday = time
                case "Sun":
                    rh.sunday = time

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clear_data),
        migrations.RunPython(seed_data)
    ]
