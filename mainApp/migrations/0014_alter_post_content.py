# Generated by Django 4.0 on 2022-03-02 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_trainingsession_cencelled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=2000),
        ),
    ]
