# Generated by Django 4.2 on 2023-05-01 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spApp', '0002_delete_favcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='result',
            field=models.CharField(max_length=500, null=True),
        ),
    ]