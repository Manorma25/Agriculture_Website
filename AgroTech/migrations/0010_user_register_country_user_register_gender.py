# Generated by Django 5.0.1 on 2024-08-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "AgroTech",
            "0009_alter_user_register_address_alter_user_register_dob_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="user_register",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user_register",
            name="gender",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
