# Generated by Django 3.2.4 on 2021-06-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_custompermission_granted_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='birth_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='birth date'),
        ),
    ]
