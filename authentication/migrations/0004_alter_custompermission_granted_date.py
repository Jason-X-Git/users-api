# Generated by Django 3.2.4 on 2021-06-06 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210606_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompermission',
            name='granted_date',
            field=models.DateField(auto_now=True),
        ),
    ]
