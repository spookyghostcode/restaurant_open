from . import util, models
import pytest

MONDAY="9am-5pm"
TUESDAY="closed"
WEDNESDAY="9am-4pm"
THURSDAY="9am-2am"
FRIDAY="11:30am-11:30pm"
SATURDAY="closed"
SUNDAY="1pm-6pm"

@pytest.fixture
def restaurant():
    rh = models.RestaurantHours(name="Test Rest",
                         monday=MONDAY,
                         tuesday=TUESDAY,
                         wednesday=WEDNESDAY,
                         thursday=THURSDAY,
                         friday=FRIDAY,
                         saturday=SATURDAY,
                         sunday=SUNDAY)
    
    return rh

@pytest.mark.parametrize("day, hours", [
    (0, MONDAY),
    (1, TUESDAY),
    (2, WEDNESDAY),
    (3, THURSDAY),
    (4, FRIDAY),
    (5, SATURDAY),
    (6, SUNDAY),
])
def test_fetch_hours_success(restaurant, day, hours):
    assert util.fetch_hours(day, restaurant) == hours


def test_fetch_hours_fail(restaurant):
    with pytest.raises(ValueError):
        util.fetch_hours(9, restaurant)

@pytest.mark.parametrize("day, correct_output", [
    (0, 6),
    (1, 0),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 5),
])
def test_decrement_weekday_success(day, correct_output):
    assert util.decrement_weekday(day) == correct_output

def test_decrement_weekday_fail():

    with pytest.raises(ValueError):
        util.decrement_weekday(9)