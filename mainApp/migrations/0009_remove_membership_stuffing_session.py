# Generated by Django 4.0 on 2022-02-26 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_post_approved_post_club'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='stuffing_session',
        ),
    ]