# Generated by Django 2.2.28 on 2024-03-14 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodieshare', '0003_auto_20240314_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='https://t4.ftcdn.net/jpg/02/29/75/83/360_F_229758328_7x8jwCwjtBMmC6rgFzLFhZoEpLobB6L8.jpg', upload_to=''),
        ),
    ]
