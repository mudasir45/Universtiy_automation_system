# Generated by Django 4.1.3 on 2023-05-20 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_attendence_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='CNIC',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='smester',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
