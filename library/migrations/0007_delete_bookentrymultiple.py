# Generated by Django 2.2.5 on 2019-09-27 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_remove_bookprofiledetails_subject'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookEntryMultiple',
        ),
    ]
