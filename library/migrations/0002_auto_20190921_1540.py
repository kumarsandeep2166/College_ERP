# Generated by Django 2.2.5 on 2019-09-21 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomno',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
