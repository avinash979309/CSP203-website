# Generated by Django 5.1.1 on 2024-10-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_skill_rating_count_skillrequest_skilltrade_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/'),
        ),
    ]