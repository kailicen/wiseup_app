# Generated by Django 2.2 on 2022-03-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220310_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='if_private',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
