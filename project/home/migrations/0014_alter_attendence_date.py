# Generated by Django 4.2.1 on 2023-05-20 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_attendence_lacture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='date',
            field=models.DateField(),
        ),
    ]
