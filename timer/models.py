from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class Race(models.Model):
    description = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    total_racers = models.SmallIntegerField()
    distance = models.IntegerField()
    director = models.CharField(max_length=50)
    # director_id = models.ForeignKey(User, on_delete=models.CASCADE)
    safety_officer = models.CharField(max_length=50)

    def __str__(self):
        # return self.description[:10]
        return self.description


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    swims_in = models.ManyToManyField(Race, related_name="swims_in",
                                      symmetrical=False, blank=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )

    def __str__(self):
        return self.user.username




class Handicap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hcap = models.SmallIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.user.username


class Times(models.Model):
    place = models.SmallIntegerField()
    time = models.FloatField()
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.place)


class Chips(models.Model):
    place = models.SmallIntegerField()
    swimmer = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)


class Results(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    swimmer = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField()
    place = models.IntegerField()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()
