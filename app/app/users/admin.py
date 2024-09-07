from django.contrib import admin

from app.users.models import Follow, User

class FollowerTabular(admin.StackedInline):
    model = Follow
    extra = 0
    fk_name = "follower" 

class FollowingTabular(admin.StackedInline):
    model = Follow
    extra = 0
    fk_name = "following" 

class UserAdmin(admin.ModelAdmin):
    inlines = [FollowerTabular, FollowingTabular]

class FollowAdmin(admin.ModelAdmin):
    list_display = ["id", "follower", "following"]

admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)