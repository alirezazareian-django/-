# Generated by Django 5.1.3 on 2024-12-14 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
