from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Location)
admin.site.register(Coupon)
admin.site.register(Game)
admin.site.register(GameInvitation)
admin.site.register(UserProfile)
admin.site.register(GameLocation)
admin.site.register(LocationQuestion)
admin.site.register(GameQuestion)
