# Generated by Django 3.2.7 on 2021-09-23 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='request_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
