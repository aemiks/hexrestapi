from django.contrib import admin
from .models import UserPlans, UserImages, CustomThumbnail, LinkExpiresTime, Profile, ShowOriginalLink
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_tier',)

class CustomThumbnailInline(admin.TabularInline):
    model = CustomThumbnail
    extra = 1
    max_num = 2

class ShowOriginalLinkInline(admin.StackedInline):
    model = ShowOriginalLink

class LinkExpiresTimeInline(admin.StackedInline):
    model = LinkExpiresTime

class UserPlansAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        CustomThumbnailInline, ShowOriginalLinkInline,  LinkExpiresTimeInline
    ]

admin.site.register(UserPlans, UserPlansAdmin)
admin.site.unregister(Group)
admin.site.register(Profile, ProfileAdmin)

@admin.register(UserImages)
class UserImagesAdmin(admin.ModelAdmin):
    """
    slug field is added for future improvements
    """
    list_display = ('title','user', 'original_image', 'slug',)
    prepopulated_fields = {'slug':('title',),}

