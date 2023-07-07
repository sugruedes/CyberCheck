from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Dweet, Profile, Race, Results, Handicap, Chips, Times


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "is_staff", "email"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Dweet)
admin.site.register(Race)
admin.site.register(Results)
admin.site.register(Handicap)
admin.site.register(Times)
admin.site.register(Chips)

