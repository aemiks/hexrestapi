# Generated by Django 3.2.7 on 2021-09-24 21:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagesapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Basic', 'Basic'), ('Premium', 'Premium'), ('Enterprise', 'Enterprise'), ('Custom', 'Custom')], default='Basic', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('published_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('original_image', models.ImageField(upload_to=imagesapp.models.upload_directory, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])], verbose_name='Original Image')),
                ('expire_time', models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)], verbose_name='Link expire time in [sec] - Only Enterprise Plan')),
                ('slug', models.SlugField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ShowOriginalLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_link_ability', models.BooleanField(default=False, verbose_name='Show original Image link')),
                ('plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='imagesapp.userplans')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
                ('user_tier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='imagesapp.userplans')),
            ],
        ),
        migrations.CreateModel(
            name='LinkExpiresTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_presence', models.BooleanField(default=False, verbose_name='Ability to generate expire link')),
                ('expire_time', models.PositiveIntegerField(default=300, verbose_name='Link expire time in [sec]')),
                ('plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='link_expire', to='imagesapp.userplans')),
            ],
        ),
        migrations.CreateModel(
            name='CustomThumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail_name', models.CharField(blank=True, max_length=30)),
                ('thumbnail_height', models.PositiveIntegerField(default=200)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnail', to='imagesapp.userplans')),
            ],
        ),
    ]
