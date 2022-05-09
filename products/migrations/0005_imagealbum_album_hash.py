# Generated by Django 4.0.3 on 2022-05-08 22:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_imagealbum_album_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagealbum',
            name='album_hash',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='album hash'),
        ),
    ]
