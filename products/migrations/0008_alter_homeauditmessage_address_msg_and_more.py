# Generated by Django 4.0.3 on 2022-06-13 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_home_tags_alter_home_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeauditmessage',
            name='address_msg',
            field=models.TextField(blank=True, null=True, verbose_name='address message'),
        ),
        migrations.AlterField(
            model_name='homeauditmessage',
            name='album_msg',
            field=models.TextField(blank=True, null=True, verbose_name='album message'),
        ),
        migrations.AlterField(
            model_name='homeauditmessage',
            name='apartment_type_msg',
            field=models.TextField(blank=True, null=True, verbose_name='aparment type message'),
        ),
        migrations.AlterField(
            model_name='homeauditmessage',
            name='price_msg',
            field=models.TextField(blank=True, null=True, verbose_name='price message'),
        ),
        migrations.AlterField(
            model_name='homeauditmessage',
            name='selling_point_msg',
            field=models.TextField(blank=True, null=True, verbose_name='selling point message'),
        ),
        migrations.AlterField(
            model_name='homeauditmessage',
            name='short_description_msg',
            field=models.TextField(blank=True, null=True, verbose_name='short description message'),
        ),
    ]
