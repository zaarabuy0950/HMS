# Generated by Django 3.2.3 on 2021-05-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='profile_pic',
            field=models.ImageField(blank=True, default='static/images/logo.jpeg', null=True, upload_to=''),
        ),
    ]
