def fetch_hours(date, rest):
    match date:
        case 0:
            return rest.monday
        case 1:
            return rest.tuesday
        case 2:
            return rest.wednesday
        case 3:
            return rest.thursday
        case 4:
            return rest.friday
        case 5:
            return rest.saturday
        case 6:
            return rest.sunday
        case _:
            raise ValueError("Invalid date: Number must be between 0-6")
        
def decrement_weekday(date):
        if date < 0 or date > 6:
            raise ValueError("Invalid date: Number must be between 0-6")
        date -= 1
        if date < 0:
            date = 6
        
        return date