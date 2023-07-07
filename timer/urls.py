from django.urls import path
from .views import dashboard, profile_list, profile, timer, race_list
from .views import add_swimmer_to_race
app_name = "timer"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("timer/<int:race_id>", timer, name="timer"),
    path("race_list/", race_list, name="race_list"),
    path("add_swimmer_to_race/<int:race_id>", add_swimmer_to_race, name="add_swimmer_to_race"),
]
