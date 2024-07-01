import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("value, name", [
    ("Jan 1 2024 11pm", "Caffe Luna"),
    ("Jan 2 2024 3:45am", "Seoul 116"),
    ("Jan 6 2024 4:00pm", "Bonchon"),
    ("Jan 7 2024 10:45pm", "Mandolin"),
    ("Jan 6 2024 10:45pm", "Oakleaf"),
    ("Jan 3 2024 12pm", "Stanbury")

])
def test_restaurant_open(client, value, name):
    url = reverse('get-restaurants')
    resp = client.get(url, {"datetime": value})
    assert resp.status_code == 200
    assert resp.json()['Open Restaurants'] is not None
    assert name in resp.json()['Open Restaurants']

@pytest.mark.parametrize("param, value", [
    ("date", "Jan 1 2024 11pm"),
    ("datetime", "January 1 2024 11pm"),
    ("datetime", "Jan 1st 2024 11pm"),
    ("time", "Jan 1 2024 11pm"),
    ("datetime", "Jan 1 2024 11 pm"),
    ("datetime", "Jan 1 2024 11:300pm"),
])
def test_restaurant_open_bad_params(client, param, value):
    url = reverse('get-restaurants')
    resp = client.get(url)
    assert resp.status_code == 400

    resp = client.get(url, {param: value})
    assert resp.status_code == 400