# Generated by Django 4.0.4 on 2022-05-11 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
