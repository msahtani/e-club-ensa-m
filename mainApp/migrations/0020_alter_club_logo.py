# Generated by Django 4.0 on 2022-03-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0019_alter_club_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.ImageField(upload_to='mainApp/static/images/club_logos'),
        ),
    ]
