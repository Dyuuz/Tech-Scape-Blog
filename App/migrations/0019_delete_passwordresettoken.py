# Generated by Django 5.1.6 on 2025-02-09 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_passwordresettoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PasswordResetToken',
        ),
    ]
