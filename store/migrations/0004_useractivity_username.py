# Generated by Django 5.1.1 on 2024-09-23 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_useractivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='username',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
