# Generated by Django 4.1.3 on 2023-05-18 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='gpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='gpa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpa', models.FloatField(blank=True, null=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
    ]
