# Generated by Django 4.1.3 on 2023-05-18 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_marks_gpa_gpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpa',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.student'),
        ),
    ]
