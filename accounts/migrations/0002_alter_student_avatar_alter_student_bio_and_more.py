# Generated by Django 4.0.3 on 2022-04-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='image/avatars'),
        ),
        migrations.AlterField(
            model_name='student',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]