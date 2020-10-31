# Generated by Django 3.1.2 on 2020-10-30 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20201030_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0.25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes',
                                                 to='api.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
