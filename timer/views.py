from django.shortcuts import render, redirect

from .forms import DweetForm, RaceForm
from .models import Dweet, Profile, Times, Race


def dashboard(request):
    form = DweetForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("timer:dashboard")

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "timer/dashboard.html",
        {"form": form, "dweets": followed_dweets},
    )


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "timer/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "timer/profile.html", {"profile": profile})


def timer(request, race_id):
    race = Race.objects.get(pk=race_id)
    times = Times.objects.filter(race_id=race_id).order_by('-place')
    print("This is a Timer event")
    if request.method == "POST":
        data = request.POST
        form_time = data.get("time_button")
        record = Times()
        record.time = form_time
        try:
            curr_place = Times.objects.filter(race=race_id).latest('place')
            # print("Current place is %d", curr_place.place)
            record.place = curr_place.place + 1
        except:
            record.place = 1

        record.race = race
        record.save()
        return redirect(request.path_info)

    return render(request, 'timer/timer.html', {"times": times})


def race_list(request):
    races = Race.objects.all()
    return render(request, "timer/race_list.html", {"races": races})


def add_swimmer_to_race(request, race_id):
    form = RaceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            swimmers = request.POST.getlist('swimmers')
            for swimmer in swimmers:
                record = Profile.objects.get(pk=swimmer)
                record.swims_in.add(race_id)

            return redirect(request.path_info)

    form = RaceForm(race_id=race_id)
    race = Race.objects.get(pk=race_id)
    # swimmers = Profile.objects.all()
    return render(request, "timer/add_swimmer_to_race.html", {  # "swimmers": swimmers,
                                                              "race_id": race,
                                                              "form": form})
