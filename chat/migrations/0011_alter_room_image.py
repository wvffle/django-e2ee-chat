# Generated by Django 3.2 on 2021-06-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_alter_room_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='room_images'),
        ),
    ]
