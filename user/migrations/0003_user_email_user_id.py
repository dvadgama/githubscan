# Generated by Django 3.2.12 on 2022-02-22 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_user_id",
            field=models.EmailField(
                blank=True, max_length=254, unique=True, verbose_name="email address"
            ),
        ),
    ]
