# Generated by Django 3.2.3 on 2021-05-30 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210529_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
    ]
