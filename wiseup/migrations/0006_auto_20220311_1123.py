# Generated by Django 2.2 on 2022-03-11 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiseup', '0005_auto_20220310_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(),
        ),
    ]
