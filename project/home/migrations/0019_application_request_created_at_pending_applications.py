# Generated by Django 4.1.3 on 2023-05-21 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_application_request_hod_alter_hod_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application_request',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='pending_applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.application_request')),
            ],
        ),
    ]
