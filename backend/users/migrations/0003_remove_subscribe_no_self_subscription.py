# Generated by Django 3.2.16 on 2024-04-08 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240408_1725'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='no_self_subscription',
        ),
    ]
