from django.db import models
from django.utils import timezone
from datetime import datetime as dt
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserPlans(models.Model):
    """
    Class responsible for create Arbitary Plan
    with thumbnail heights and ability to generate original and expire images links.
    """
    class Tiers(models.TextChoices):
        """
        Types of user plan tier
        """
        BASIC = "Basic", "Basic"
        PREMIUM = "Premium", "Premium"
        ENTERPRISE = "Enterprise", "Enterprise"
        CUSTOM = "Custom", "Custom"

    name = models.CharField(max_length=50, choices=Tiers.choices, default=Tiers.BASIC)

    def __str__(self):
        return str(self.name)

class CustomThumbnail(models.Model):
    plan = models.ForeignKey(UserPlans, related_name='thumbnail', on_delete=models.CASCADE)
    thumbnail_name = models.CharField(max_length=30, blank=True)
    thumbnail_height = models.PositiveIntegerField(default=200)

    def __str__(self):
        return self.thumbnail_name

class ShowOriginalLink(models.Model):
    plan = models.OneToOneField(UserPlans, on_delete=models.CASCADE)
    show_link_ability = models.BooleanField(_("Show original Image link"), default=False)

    def __str__(self):
        return str(self.show_link_ability)

class LinkExpiresTime(models.Model):
    plan = models.OneToOneField(UserPlans, related_name='link_expire', on_delete=models.CASCADE)
    link_presence = models.BooleanField(_("Ability to generate expire link"),default=False)
    expire_time = models.PositiveIntegerField(_("Link expire time in [sec]"), default=300)

    def __str__(self):
        return str(self.link_presence)

class Profile(models.Model):
    """
    The Profile model inherits the user from the User model, allow to add User Plan
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    user_tier = models.ForeignKey(UserPlans, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

def upload_directory(instance, filename):
    """
    function to define where we want to upload an original image file
    Returns:
        uploads the file into the usersimage folder and subfolders with the current upload date
    """
    _now = dt.now()
    return 'usersimages/{year}/{month_date}/{filename}'.format(
        filename=filename, year=_now.strftime('%Y'), month_date=_now.strftime('%m%d')
        )

class UserImages(models.Model):
    """
    Image model allows to upload image and set tittle, gives possiblity to display 2 thumbnail(depends on user tier)
    and add expire time to fetch links in enterprise plan
    """
    title = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now, blank=True)
    original_image = models.ImageField(_('Original Image'),
                                        upload_to=upload_directory,
                                        validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])]
                                       )
    expire_time = models.PositiveIntegerField(_("Link expire time in [sec] - Only Enterprise Plan"),
                                              blank=True,
                                              default=0,
                                              validators=[
                                                  MinValueValidator(300),
                                                  MaxValueValidator(30000),
                                                ]
                                              )
    slug = models.SlugField(max_length=150, null=True, blank=True)
    first_thumbnail = ImageSpecField(source='original_image',
                                     processors=[ResizeToFill(200, 200)]
                                     )
    second_thumbnail = ImageSpecField(source='original_image',
                                     processors=[ResizeToFill(400,400)],
                                     )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    After create User automatically add to Profile
    """
    try:
        if created:
            Profile.objects.create(user=instance).save()
    except Exception as err:
        print('Error creating user profile!')

@receiver(post_save, sender=User)
def create_basic_userplan(sender, instance, created, **kwargs):
    """
    Automatic(after user create) creation of Basic plan and adding it to the user
    """
    try:
        if created:
            if UserPlans.objects.filter(name=UserPlans.Tiers.BASIC).exists():
                basic = UserPlans.objects.filter(name=UserPlans.Tiers.BASIC).get()
                profile = Profile.objects.filter(user=instance).get()
                profile.user_tier = basic
                profile.save()
            else:
                UserPlans.objects.create(name=UserPlans.Tiers.BASIC)
                basic = UserPlans.objects.filter(name=UserPlans.Tiers.BASIC).get()
                CustomThumbnail.objects.create(plan=basic, thumbnail_name='Basic', thumbnail_height=200)
                profile = Profile.objects.filter(user=instance).get()
                profile.user_tier = basic
                profile.save()
    except Exception as err:
        print('Error creating Basic plan!')

@receiver(post_save, sender=User)
def create_premium_userplan(sender, instance, created, **kwargs):
    """
    Automatic creation of Premium plan(after User post_save)
    """
    try:
        if created:
            if UserPlans.objects.filter(name=UserPlans.Tiers.PREMIUM).exists():
                pass
            else:
                UserPlans.objects.create(name=UserPlans.Tiers.PREMIUM)
                premium = UserPlans.objects.filter(name=UserPlans.Tiers.PREMIUM).get()
                CustomThumbnail.objects.create(plan=premium, thumbnail_name='Basic', thumbnail_height=200)
                CustomThumbnail.objects.create(plan=premium, thumbnail_name='Premium', thumbnail_height=400)
                ShowOriginalLink.objects.create(plan=premium, show_link_ability=True)
    except Exception as err:
        print('Error creating Premium plan!')

@receiver(post_save, sender=User)
def create_enterprise_userplan(sender, instance, created, **kwargs):
    """
    Automatic creation of Enterprise plan(after User post_save)
    """
    try:
        if created:
            if UserPlans.objects.filter(name=UserPlans.Tiers.ENTERPRISE).exists():
                pass
            else:
                UserPlans.objects.create(name=UserPlans.Tiers.ENTERPRISE)
                enterprise = UserPlans.objects.filter(name=UserPlans.Tiers.ENTERPRISE).get()
                CustomThumbnail.objects.create(plan=enterprise, thumbnail_name='Basic', thumbnail_height=200)
                CustomThumbnail.objects.create(plan=enterprise, thumbnail_name='Premium', thumbnail_height=400)
                ShowOriginalLink.objects.create(plan=enterprise, show_link_ability=True)
                LinkExpiresTime.objects.create(plan=enterprise, link_presence=True)
    except Exception as err:
        print('Error creating Premium plan!')