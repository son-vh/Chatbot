# Generated by Django 2.1.4 on 2019-01-28 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingroom',
            name='status',
            field=models.IntegerField(),
        ),
    ]
